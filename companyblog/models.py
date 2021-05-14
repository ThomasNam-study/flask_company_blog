from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from companyblog import db, login_manage


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')

    email = db.Column(db.String(64), unique=True, index=True)

    username = db.Column(db.String(54), unique=True)

    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class BlogPost(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, userid):
        self.title = title
        self.text = text
        self.user_id = userid

    def __repr__(self):
        return f"Post ID : {self.id} -- Date : {self.date}"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    create_date = db.Column(db.DateTime(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))

    modify_date = db.Column(db.DateTime(), nullable=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', ))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))

    modify_date = db.Column(db.DateTime(), nullable=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))

    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('comment_set', ))

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'))
    answer = db.relationship('Answer', backref=db.backref('comment_set', ))