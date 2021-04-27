from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required             
from flaskblog.models import Post              
from flaskblog.posts.forms import PostForm     
from flaskblog import db                                        


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created !', 'success')

        return redirect(url_for('main.home'))

    return render_template('pages/create_post.html', title='New Post', 
                            form=form, legend='New Post')



@posts.route("/post/<int:post_id>")  #or "/post/<post_id>"
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('pages/post.html', title=post.title, post=post)


#you cant have the same function name for multiple routes... 

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():           #if the update form was being sent... 
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()                 #since you are just updating something that is in the database... 
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':       #populate the form with those values... 
        form.title.data = post.title
        form.content.data = post.content

    return render_template('pages/create_post.html', title='Update Post', 
                            form=form, legend='Update Form')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)     #delete post.. 
    db.session.commit()

    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))



