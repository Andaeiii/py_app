import os
import secrets  
from PIL import Image  
from flask import url_for
from flaskblog import app, mail
from flask_mail import Message 


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)                     # files have attributes...  _  is used to discard variables... 
    picture_fn = random_hex + f_ext                                             # new name + extension...     
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)    # absolute url for file path... 

    # saves pic to folder...
    # form_picture.save(picture_path)   # directly upload image.. 
    #
    # resize picture..
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)            # save the resized thumbnail..
                                          

    return picture_fn   #to use the filename 




#email to send emails... 
def send_reset_email(user):
    token = user.get_reset_token()  #default = 1800 - 30 seconds. 
    msg = Message('Password Reset Request', 
                   sender='noreply@dem.com', 
                   recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}


if you did not make this request, then simply ignore this email and no changes will be made
'''
# external=True - for absolute URLs.. ~ for full domains.. 

    mail.send(msg)   # send the mail here...