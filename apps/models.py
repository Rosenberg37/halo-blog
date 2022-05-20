# coding: utf-8
from datetime import datetime

from flask_login import UserMixin

from apps.extentions import db
from apps.extentions import login_manager
from apps.util import common


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

    @staticmethod
    def verity_password(origin_password, password):
        new_password = common.md5(origin_password)
        return password == new_password

    def __repr__(self):
        return '<User %r>' % self.username


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    desc = db.Column(db.String(64), nullable=True)
    count = db.Column(db.Integer, nullable=False, default=1)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.name

