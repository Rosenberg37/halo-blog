# coding:utf-8
from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_bootstrap import Bootstrap5

from flask_moment import Moment
import config
from apps.blog import blog
from apps.extentions import db, login_manager
from apps.model_view import UserModelView, BaseMView, ArticleVModel, CommentView, FileAdminView
from apps.models import User, Tag, Article, Comment
import os.path as op

from config import *
import pymysql as mysql

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    # 注册蓝图
    app.register_blueprint(blog)

    # 注册db
    db.init_app(app)
    db.create_all(app=app)

    # 汉化
    babel = Babel(app)

    moment = Moment(app)
    # Bootstrap
    bootstrap = Bootstrap5(app)

    # 注册flask-admin
    admin = Admin(app, name="HaloBlog", template_mode='bootstrap3', base_template='admin/mybase.html')

    admin.add_view(UserModelView(User, db.session, name="用户管理"))
    admin.add_view(BaseMView(Tag, db.session, category='Models', name="标签管理"))
    admin.add_view(ArticleVModel(Article, db.session, category='Models', name="文章管理"))
    admin.add_view(CommentView(Comment, db.session, category='Models', name='评论管理'))
    path = op.join(op.dirname(__file__), 'static/uploadfile')
    admin.add_view(FileAdminView(path, '/static/uploadfile', name='Static Files'))
    # 整合flask-login
    login_manager.init_app(app)

    #   add an admin user

    con = mysql.connect(host=HOST, port=3306, user=USERNAME, passwd=PASSWORD, db=DATABASE, charset="utf8mb4")
    mycursor = con.cursor()
    sql = "insert into user (username, email, password_hash) values ('admin', 'null', '21232f297a57a5a743894a0e4a801fc3')"
    mycursor.execute(sql)
    con.commit()

    return app
