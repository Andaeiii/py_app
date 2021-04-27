from flask import render_template, request, Blueprint
from flaskblog.models import Post                                      


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")                                                                               # include another route...
def home():
    page = request.args.get('page', 1, type=int)                                                   # page, default page, type=integer...
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)           # all()  #order by date..
    return render_template('pages/home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('pages/about.html', title='About')

