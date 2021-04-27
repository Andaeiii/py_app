from flaskblog import routes
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_mail import Mail

import secrets
import email_validator

app = Flask(__name__)

# '13ec28b7a000d4aa9e661c009363c90efdde0a9c3d9bc014cd8ed3f2d43a32f36bf5' #CSRF TOKEN.
app.config['SECRET_KEY'] = secrets.token_hex(18)             # key changes..

# configure database here... ##SQLite DB in the python folder..
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysite.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# use to handle sessions in the application
# using the login manager to manage the applications login screen...
login_manager = LoginManager(app)
# if you're not logged in, restricted pages - redirect to " login " then adds the next-url paraments.
login_manager.login_view = 'login'
# for the bootstrap-alert message on the homepage
login_manager.login_message_category = 'info'


# CONFIGURE MAIL..
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['DEBUG'] = True

# # Flask-Security Config
# app.config['SECURITY_REGISTERABLE'] = True
# app.config['SECURITY_TRACKABLE'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
# app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_EMAIL_SENDER'] = 'andaeiii@gmail.com'

# the applications email settings...
app.config['MAIL_DEFAULT_SENDER'] = 'andaeiii@gmail.com'
app.config['MAIL_USERNAME'] = 'andaeiii@gmail.com'
app.config['MAIL_PASSWORED'] = 'WYCLEF1234'  # os.environ.get('EMAIL_USER')

mail = Mail(app)

# put the rotutes at the bottom..
