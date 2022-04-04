from flask import render_template, redirect, url_for, flash
from flask_blog import app, db
from flask_blog.forms.create_post_form import CreatePostForm

from flask_login import login_required, current_user

from flask_blog.models import Post


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash(message="Your post has been created", category="success")
        return redirect(url_for("account"))
    return render_template("create_post.html", form=form)