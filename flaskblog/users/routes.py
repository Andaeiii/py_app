from flask import render_template, url_for, flash, redirect, request, abort, Blueprint            
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required  
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.users.forms import myLoginForm, myRegForm, myUpdateAccount, RequestResetForm, ResetPasswordForm      
from flaskblog import db, bcrypt                                                         


users = Blueprint('users', __name__)


#Render Forms....
@users.route("/register", methods=['GET','POST'])
def register():

    if current_user.is_authenticated:                   # if user is already l
        return redirect (url_for('main.home'))

    form = myRegForm()
    if form.validate_on_submit():
       
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # #first string instead of bytes        
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #add user to database.
        db.session.add(user)
        db.session.commit();

        #flash them a message..
        flash('Your Account has been created! you can now login..', 'success')  #f-toinclude variables..
        return redirect(url_for('users.login'))        # redirect to name of route..

    return render_template('pages/register.html', title='Register', form=form)



@users.route("/login", methods=['GET','POST'])   #handle login forms...
def login():
    
    if current_user.is_authenticated:                   # if user is already logged-in, redirect to home..
        return redirect (url_for('main.home'))

    form = myLoginForm()
    if form.validate_on_submit():

        #check if user exist... 
        user = User.query.filter_by(email=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))   # tenary operator in python...
        else:    
            flash('login unsuccessful, pls check usrname and password', 'danger')    
  
    return render_template('pages/login.html', title='Login', form=form)  #then render-template if error in form submission.....

    

'''if form.username.data == 'admin@blog.com' and form.password.data == 'password':
    flash('you have been logged in!', 'success')
    return redirect(url_for('main.home'))
else:'''



@users.route("/logout")
def logout():
    logout_user();
    return redirect(url_for('main.home'))





@users.route("/account",  methods=['GET','POST'])
@login_required
def account():
    form = myUpdateAccount()

    if form.validate_on_submit():
        if form.picture.data:                            # check if it has a picture file..
            current_user.image_file = save_picture(form.picture.data)       # pass the new name to the current user object...

        current_user.username = form.username.data;
        current_user.email = form.email.data

        db.session.commit();
        flash('your account has been updated', 'success')
        return redirect(url_for('users.account'))             #...to avoid a post/get/redirect error... 

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data    = current_user.email

    imgfile = url_for('static', filename='uploads/' + current_user.image_file)
    return render_template('pages/account.html', title='AccountPage', profile_pix=imgfile, form=form)




@users.route("/user/<string:username>")                                          #  include another route...
def user_posts(username):
    
    page = request.args.get('page', 1, type=int)                            #   page, default page, type=integer...    
    user = User.query.filter_by(username=username).first_or_404()    
                                                                            #   backslash to go to a new line ~ no Spaces... 
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=2)           #.all()  #order by date..

    return render_template('pages/user_posts.html', posts=posts, user=user)    





@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:                   # so they are logged out before they change their password..
       return redirect (url_for('main.home'))
      
    form = RequestResetForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()       # first user with that email..
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('pages/reset_request.html', title='Reset Password', form=form)  




@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:                  
       return redirect (url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None: 
       flash('that is an invalid or expired token', 'warning')
       return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():           
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # #first string instead of bytes        
        user.password = hashed_password
        db.session.commit();

        #flash them a message..
        flash('Your password has been updated..', 'success')  #f-toinclude variables..
        return redirect(url_for('users.login'))        # redirect to name of route..


    return render_template('pages/reset_token.html', title='Reset Password', form=form)  