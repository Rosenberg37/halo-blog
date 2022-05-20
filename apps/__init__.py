# coding:utf-8
from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_bootstrap import Bootstrap

import config
from apps.blog import blog
from apps.extentions import db, login_manager
from apps.model_view import UserModelView, BaseMView, ArticleVModel, CommentView
from apps.models import User, Tag, Article, Comment


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

    # Bootstrap
    bootstrap = Bootstrap(app)

    # 注册flask-admin
    admin = Admin(app, name="HaloBlog", template_mode='bootstrap3', base_template='admin/mybase.html')

    admin.add_view(UserModelView(User, db.session, name="用户管理"))
    admin.add_view(BaseMView(Tag, db.session, category='Models', name="标签管理"))
    admin.add_view(ArticleVModel(Article, db.session, category='Models', name="文章管理"))
    admin.add_view(CommentView(Comment, db.session, category='Models', name='评论管理'))

    # 整合flask-login
    login_manager.init_app(app)

    return app
