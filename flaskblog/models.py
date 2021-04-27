from flaskblog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin  # to add the extra fields..
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer       # for Timed Tokens... 


@login_manager.user_loader     #decorator so extension flask_login - knows this is the function to get the user by id..
def load_user(user_id):
    return User.query.get(int(user_id))

#sqlalchemy dbases as classes... 
class User(db.Model, UserMixin):
    #__tablename__ = 'users'  #tells sqlalchemy tablename to use...
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(20), unique=True, nullable=False)
    email           = db.Column(db.String(30), unique=True, nullable=False)
    password        = db.Column(db.String(60), nullable=False)
    image_file      = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts           = db.relationship('Post', backref='author', lazy=True)             # one-to-many relationship...

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
    def get_reset_token(self, expires_sec=1800):                #30mins
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:                                                    #the token could be invalid or time expired or somerhing..
            user_id = s.loads(token)['user_id']
        except:
            return None                                         # if we get an exception it returnsns none... 

        return User.query.get(user_id)

        


class Post(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # (table name . column name)
    title           = db.Column(db.String(120), nullable=False)
    date_posted     = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow)
    content         = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
       
