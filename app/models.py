import uuid
from flask_security import UserMixin, RoleMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    unique_identifier = db.Column(
        db.String(36), default=str(uuid.uuid4()), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean(), default=True)

    def repr(self):
        return 'User ' + str(self.id)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), unique=True, nullable=False)

    def repr(self):
        return 'Role ' + str(self.id)


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    attachment = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(
        db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(
        'feedbacks', lazy=True, cascade='all, delete'))

    def repr(self):
        return 'Feedback ' + str(self.id)


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'users.id'), primary_key=True),
                      db.Column('role_id', db.Integer, db.ForeignKey(
                          'roles.id'), primary_key=True)
                      )