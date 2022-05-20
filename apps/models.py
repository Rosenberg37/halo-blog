# coding: utf-8
from datetime import datetime

from flask_login import UserMixin

from apps.extentions import db
from apps.extentions import login_manager


# 用户表
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    role = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(128))
    head_img = db.Column(db.String(128), unique=False, nullable=True)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    @staticmethod
    @login_manager.user_loader
    def load_user(userid):
        user = User.query.filter_by(id=userid).first()
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    comments = db.relationship('Comment', back_populates='article', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    article = db.relationship('Article', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    desc = db.Column(db.String(64), nullable=True)
    count = db.Column(db.Integer, nullable=False, default=1)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.name
