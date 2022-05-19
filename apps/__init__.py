# coding:utf-8
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # 注册蓝图
    from apps.blog import blog
    app.register_blueprint(blog)

    # 注册db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Blog@2022@114.55.252.134:3306/blog'
    db.init_app(app)

    # 国际化
    from flask_babelex import Babel
    babel = Babel(app)

    # 注册flask-admin
    admin = Admin(app, name="xiaoblog", template_mode='bootstrap3', base_template='admin/mybase.html')
    from .models import User, Tag, Article
    from apps.modelview import UModelview, BaseMView, ArticleVModel

    admin.add_view(UModelview(User, db.session, name="用户管理"))
    admin.add_view(BaseMView(Tag, db.session, category='Models', name="标签管理"))
    admin.add_view(ArticleVModel(Article, db.session, category='Models', name="文章管理"))

    # 整合flask-login
    login_manager.init_app(app)

    app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'

    return app
