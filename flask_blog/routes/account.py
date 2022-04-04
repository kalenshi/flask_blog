import os
import secrets

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from PIL import Image

from flask_blog import app, db
from flask_blog.forms import UpdateAccountForm

image_dir = os.path.join(app.root_path, "static", "images")
picture_dimensions = (125, 125)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    profile_filename = random_hex + file_ext
    picture_path = os.path.join(image_dir, profile_filename)

    with Image.open(form_picture) as i:
        i.thumbnail(picture_dimensions)
        i.save(picture_path)
    return profile_filename


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    profile_image = url_for("static", filename=f"images/{current_user.image_file}")

    if form.validate_on_submit():
        if form.profile.data:
            profile_filename = save_picture(form.profile.data)
            current_user.image_file = profile_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(message="Your account has been updated!", category="success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form, profile_image=profile_image)