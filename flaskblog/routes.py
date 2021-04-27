# to grab the extensions of files...
import os
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import (myLoginForm, myRegForm, myUpdateAccount,
                             PostForm, RequestResetForm, ResetPasswordForm)  # use () to break imports to multiple lines...
from flaskblog.models import User, Post
# import login_user function...
from flask_login import login_user, logout_user, current_user, login_required

from flaskblog import app, db, bcrypt, mail
import secrets  # for passwords, filenames, hex random chars..

from PIL import Image  # for resizing images...

from flask_mail import Message


@app.route("/")
@app.route("/home")  # include another route...
def home():
    # page, default page, type=integer...
    page = request.args.get('page', 1, type=int)

    # .all()  #order by date..
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=2)

    return render_template('pages/home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('pages/about.html', title='About')


# Render Forms....
@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:                   # if user is already l
        return redirect(url_for('home'))

    form = myRegForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')  # first string instead of bytes
        # add user to database.
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # flash them a message..
        # f-toinclude variables..
        flash('Your Account has been created! you can now login..', 'success')
        return redirect(url_for('login'))        # redirect to name of route..

    return render_template('pages/register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])  # handle login forms...
def login():

    # if user is already logged-in, redirect to home..
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = myLoginForm()
    if form.validate_on_submit():

        # check if user exist...
        user = User.query.filter_by(email=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            # tenary operator in python...
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('login unsuccessful, pls check usrname and password', 'danger')

    # then render-template if error in form submission.....
    return render_template('pages/login.html', title='Login', form=form)


'''if form.username.data == 'admin@blog.com' and form.password.data == 'password':
    flash('you have been logged in!', 'success')
    return redirect(url_for('home'))
else:'''


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


''''''


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # files have attributes...  _  is used to discard variables...
    f_name, f_ext = os.path.splitext(form_picture.filename)
    # new name + extension...
    picture_fn = random_hex + f_ext
    # absolute url for file path...
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

    # saves pic to folder...
    # form_picture.save(picture_path)   # directly upload image..
    #
    # resize picture..
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)            # save the resized thumbnail..

    return picture_fn  # to use the filename


@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = myUpdateAccount()

    if form.validate_on_submit():
        # check if it has a picture file..
        if form.picture.data:
            # pass the new name to the current user object...
            current_user.image_file = save_picture(form.picture.data)

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('your account has been updated', 'success')
        # ...to avoid a post/get/redirect error...
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    imgfile = url_for('static', filename='uploads/' + current_user.image_file)
    return render_template('pages/account.html', title='AccountPage', profile_pix=imgfile, form=form)


'''
    handle the CRUD operations... 

'''


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():

        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created !', 'success')

        return redirect(url_for('home'))

    return render_template('pages/create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")  # or "/post/<post_id>"
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('pages/post.html', title=post.title, post=post)


# you cant have the same function name for multiple routes...

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():  # if the update form was being sent...
        post.title = form.title.data
        post.content = form.content.data
        # since you are just updating something that is in the database...
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':  # populate the form with those values...
        form.title.data = post.title
        form.content.data = post.content

    return render_template('pages/create_post.html', title='Update Post',
                           form=form, legend='Update Form')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)  # delete post..
    db.session.commit()

    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")  # include another route...
def user_posts(username):

    # page, default page, type=integer...
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    #   backslash to go to a new line ~ no Spaces...
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)  # .all()  #order by date..

    return render_template('pages/user_posts.html', posts=posts, user=user)


# email to send emails...
def send_reset_email(user):
    token = user.get_reset_token()  # default = 1800 - 30 seconds.
    msg = Message('Password Reset Request',
                  sender='noreply@dem.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}


if you did not make this request, then simply ignore this email and no changes will be made
'''
# external=True - for absolute URLs.. ~ for full domains..

    mail.send(msg)   # send the mail here...


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # so they are logged out before they change their password..
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        # first user with that email..
        user = User.query.filter_by(email=form.username.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('pages/reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('that is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')  # first string instead of bytes
        user.password = hashed_password
        db.session.commit()

        # flash them a message..
        # f-toinclude variables..
        flash('Your password has been updated..', 'success')
        return redirect(url_for('login'))        # redirect to name of route..

    return render_template('pages/reset_token.html', title='Reset Password', form=form)
