from flask import render_template, request, redirect
from app import app, db
from app.models import Data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comments', methods=['POST', 'GET'])
def comments():
    if request.method == 'POST':
        db.session.add(Data(
            comment=request.form['comment'],
        ))
        db.session.commit()
        return redirect('/comments')
   
    comments = Data.query.all()
    return render_template('comments.html', comments=comments)

@app.route('/comments/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    comment_obj = Data.query.get(id)
    if request.method == 'POST':
        comment_obj.comment = request.form['comment']
        db.session.commit()
        return redirect('/comments')
    
    return render_template('edit.html', comment=comment_obj)

@app.route('/comments/delete/<int:id>')
def delete(id):
    comment_obj = Data.query.get(id)
    db.session.delete(comment_obj)
    db.session.commit()
    return redirect('/comments')
