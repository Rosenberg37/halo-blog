from flask_wtf import FlaskForm
from wtforms import fields, validators


class LoginForm(FlaskForm):
    username = fields.StringField(label=u'管理员账号', validators=[validators.required()])
    password = fields.PasswordField(label=u'密码', validators=[validators.required()])

    remember_me = fields.BooleanField('记住我')
    submit = fields.SubmitField('登陆')


class CommentForm(FlaskForm):
    author = fields.StringField('Name', validators=[validators.DataRequired(), validators.Length(1, 30)])
    email = fields.StringField('Email', validators=[validators.DataRequired(), validators.Email(), validators.Length(1, 254)])
    site = fields.StringField('Site', validators=[validators.Optional(), validators.URL(), validators.Length(0, 255)])
    body = fields.TextAreaField('Comment', validators=[validators.DataRequired()])
    submit = fields.SubmitField()
