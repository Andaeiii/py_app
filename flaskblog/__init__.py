from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


app = Flask(__name__)

app.config.from_object(Config) #loadConfig from this file..

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#use to handle sessions in the application
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' # if you're not logged in, restricted pages - redirect to " login " then adds the next-url paraments.
login_manager.login_message_category = 'info' #for the bootstrap-alert message on the homepage

mail = Mail(app)


# put the rotutes at the bottom.. #instance of blueprints.
from flaskblog.users.routes import users   
from flaskblog.posts.routes import posts   
from flaskblog.main.routes import main   
from flaskblog.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)