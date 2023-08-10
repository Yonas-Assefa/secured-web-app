from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db
from .models import Feedback, User, Feedback


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    last_feedbacks = Feedback.query.filter_by(user_id=current_user.id).order_by(
        Feedback.timestamp.desc()).limit(5).all()
    return render_template('dashboard.html', last_feedbacks=last_feedbacks)


@main.route('/feedback', methods=['POST', 'GET'])
@login_required
def feedback():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        attachment = request.files.get('attachment')

        if attachment:
            filename = secure_filename(attachment.filename)
            attachment.save(os.path.join('app/static/uploads', filename))
        else:
            filename = None

        feedback = Feedback(title=title, description=description,
                            attachment=filename, user_id=current_user.id)

        db.session.add(feedback)
        db.session.commit()
        flash('Feedback sent successfully', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('feedback.html')


@main.route('/all_feedbacks')
@login_required
def all_feedbacks():
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).all()
    return render_template('all_feedbacks.html', feedbacks=feedbacks)


@main.route('/edit_feedback/<int:feedback_id>', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        attachment = request.files.get('attachment')

        # Update the feedback with the new values
        feedback.title = title
        feedback.description = description

        if attachment:
            # Save the new attachment file
            filename = secure_filename(attachment.filename)
            attachment.save(os.path.join(
                'app/static/uploads', filename))
            feedback.attachment = filename
        else:
            # Clear the attachment if no new file is provided
            feedback.attachment = None

        # Save the changes to the database
        db.session.commit()

        flash('Feedback updated successfully!', 'success')
        return redirect(url_for('main.all_feedbacks'))

    return render_template('edit_feedback.html', feedback=feedback)