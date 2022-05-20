import datetime
import os
import os.path as op

import markupsafe
from flask import url_for, redirect, request
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_login.utils import current_user
from sqlalchemy.event import listens_for
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from apps.models import User, Tag
from . import db
from .util import common

file_path = op.join(op.dirname(__file__), 'static')  # 文件上传路径


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


# base ModelView
class BaseMView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


@listens_for(User, 'after_delete')
def del_image(mapper, connection, target):
    if target.head_img:
        # Delete image
        try:
            os.remove(op.join(file_path, target.head_img))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path, form.thumbgen_filename(target.head_img)))
        except OSError:
            pass


class UserModelView(BaseMView):
    # 自定义显示的column名字
    column_labels = {
        'id': u'序号',
        'email': u'邮件',
        'username': u'用户名',
        'role': u'角色',
        'password_hash': u'密码',
        'head_img': u'头像',
        'create_time': u'创建时间',
    }

    # 不显示某些字段
    # column_exclude_list = ['password_hash', ]

    def _list_thumbnail(view, context, model, name):
        if not model.head_img:
            return ''

        return markupsafe.Markup('<img src="%s">' % url_for('static', filename="uploadfile/" + form.thumbgen_filename(model.head_img)))

    column_formatters = {
        'head_img': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'head_img': form.ImageUploadField(
            'Image',
            base_path=file_path,
            relative_path="uploadfile/",
            thumbnail_size=(100, 100, True)
        )
    }

    def on_model_change(self, form, model, is_created):
        model.password_hash = common.md5(form.password_hash.data)


# 文章的自定义视图
class ArticleVModel(BaseMView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'content': CKTextAreaField
    }

    def on_model_change(self, form, model, is_created):
        print(str(model.__dict__))
        if is_created:
            tag_list = []
            if model.tag is not None:
                tag_names = model.tag.split(",")
                for tag in tag_names:
                    search_tag = Tag.query.filter_by(name=tag).first()
                    if search_tag is None:
                        tag_object = Tag(name=tag, desc=tag, count=1, create_time=datetime.datetime.utcnow())
                        tag_list.append(tag_object)
                    else:
                        search_tag.count += 1
            db.session.add_all(tag_list)
