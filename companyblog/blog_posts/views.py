from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user

from companyblog import db
from companyblog.blog_posts.forms import BlogPostForm
from companyblog.models import BlogPost

blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route("/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data, text=form.text.data, userid=current_user.id)

        db.session.add(blog_post)
        db.session.commit()

        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


@blog_posts.route("/<int:blog_post_id>")
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    return render_template('blog_post.html', post=blog_post, title=blog_post.title, date=blog_post.date)


@blog_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data

        db.session.commit()

        flash("Blog Post Update")
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()

    flash("Blog Post Deleted")

    return redirect(url_for('core.index'))
