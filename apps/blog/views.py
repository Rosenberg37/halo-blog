import sqlalchemy
from flask import url_for, redirect, request, flash, render_template, Blueprint
from flask_login import login_user, logout_user, current_user

from apps.blog.forms import LoginForm, CommentForm, AdminCommentForm
from apps.extentions import *
from apps.models import User, Article, Comment, Tag
from apps.utils import md5

blog = Blueprint('main', __name__)


@blog.route("/index")
def index():
    page = request.args.get("page")
    if page is None:
        page = 1
    page = int(page)
    # noinspection PyUnresolvedReferences
    paginate = Article.query.order_by(Article.create_time.desc()).paginate(page, 10, error_out=False)
    articles = paginate.items

    return render_template("index.html", articles=articles, paginate=paginate)


@blog.route("/")
def index2():
    return redirect(url_for("main.index"))


@blog.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password_hash == md5(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for("admin.index"))
        flash('无效的用户名或者密码')

    return render_template("login.html", form=form)


@blog.route("/login_out")
def login_out():
    logout_user()
    flash("退出成功！")
    return redirect(url_for("main.login"))


@blog.route("/about")
def about():
    return render_template("about.html")


@blog.route("/tags/<int:tag_id>")
def tags_id(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get("page")
    if page is None:
        page = 1
    page = int(page)
    paginate = Article.query.with_parent(tag).order_by(sqlalchemy.desc(Article.create_time)).paginate(page, 3,
                                                                                                      error_out=False)
    articles = paginate.items
    return render_template("tags.html", articles=articles, category=tag, paginate=paginate)


@blog.route("/tags")
def tags():
    tags = Tag.query.order_by(sqlalchemy.desc(Tag.create_time))
    cnts = [Article.query.with_parent(tag).count() for tag in tags]
    tags_list = zip(tags, cnts)
    return render_template("tags_list.html", tags_list=tags_list, cnts=cnts)


@blog.route("/article/<int:article_id>", methods=['GET', 'POST'])
def article(article_id):
    article = Article.query.get_or_404(article_id)

    pagination = Comment.query.with_parent(article).order_by(Comment.timestamp).paginate(1, 15)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.username
        form.email.data = current_user.email
        form.site.data = url_for('.index')
    else:
        form = CommentForm()

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body, article=article)

        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.article', article_id=article_id))

    return render_template('article.html', article=article, form=form, comments=comments, pagination=pagination)


@blog.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('main.article', article_id=comment.article_id, reply=comment_id,
                            author=comment.author) + '#comment-form')
