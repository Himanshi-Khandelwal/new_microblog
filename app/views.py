from app import app
from flask import Flask,render_template, redirect, request, url_for,session,escape,flash
# from .form import User
#import MySQLdb
#from db_connect import connection
from flask_oauth import OAuth
from functools import wraps
import config
from flask_login import current_user
from models import db,signup,post_data


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '188477911223606'
FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('login')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)



@app.route('/')
def home():
 return render_template("main.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function


@app.route('/welcome/<username>')
def welcome(username):
 return render_template("welcome.html")

@app.route('/post/<username>',methods=['GET','POST'])
@login_required
def post(username):
    if request.method =='POST':
         post = request.form['post']
         title = request.form['title']
         tag = request.form['tag']
         post_id = session['user_id']
         data = post_data(post, title, tag,post_id)

         db.session.add(data)
         db.session.commit()

    return render_template("post.html",username=username)

@app.route("/login/", methods=['POST','GET'])
def login():
    if request.method =='POST':
               username = request.form['username']

               password = request.form['password']
               print password, username

               user = signup.query.filter_by(username=username).first()
               print user.password
               if user!=None:
                   if user.password == password:
                        print "yooo"
                        session['logged_in']=username
                        session['user_id']=user.user_id
                        return redirect(url_for('post',username=user.username))
                   else:
                        print "NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
                        pass
               else:
			            return redirect(url_for('sign_up'))
    return render_template('login.html')


@app.route('/signup/',methods=['GET','POST'])
def sign_up():
    error=None
    if request.method == 'POST':
        user = signup(request.form['username'],request.form['email'], request.form['password'],request.form['mobile'])
        if signup.query.filter_by(username=user.username).first():
            error="Username Already exists"
        else:
            db.session.add(user)
            db.session.commit()
            #return redirect(url_for('post',username = user.username))
    return render_template("signup.html",error=error)



@app.route('/search/', methods = ['POST','GET'])
def search():
    results=None
    if request.method == 'POST':
        keyword = request.form['search']
        results = post_data.query.filter_by(title = keyword )#, post_id = session['user_id'])

    return render_template('search.html', results=results)


@app.route('/all_posts/')
def show_post():
    all_posts = post_data.query.filter_by(post_id= session['user_id'])
    return render_template('show.html', all_posts=all_posts)


@app.route("/user/<username>")
@login_required
def user(username):
    return render_template('user.html',username=username)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/delete/<title>', methods=['POST','GET'])
def delete_entry(title):
    results=None
    if request.method == 'POST':
        if title == "":
            keyword = request.form['delete']
        else:
            keyword = title
        results = post_data.query.filter_by(title = keyword ,post_id= session['user_id']).delete()
        db.session.commit()
        all_posts = post_data.query.filter_by(post_id= session['user_id'])
    return render_template('show.html', all_posts=all_posts)
