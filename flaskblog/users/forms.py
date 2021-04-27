from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed                                           #for uploads and validator(fileAllowed...)
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


#register form definition...

class myRegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #custom validators to avoid errors..

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user : 
            raise ValidationError('That Username is taken, Please Choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user : 
            raise ValidationError('That Email is taken, Please Choose another.')


class myLoginForm(FlaskForm):
    username = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

#a secret key csrf token..     


class myUpdateAccount(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Account')

    #custom validators to avoid errors..
    #only validate if the new values are different from the db_values.. 

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user : 
                raise ValidationError('That Username is taken, Please Choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user : 
                raise ValidationError('That Email is taken, Please Choose another.')



class RequestResetForm(FlaskForm):
    username = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
 
    def validate_email(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is None : 
            raise ValidationError('There is no account with that email, you must register first...')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    