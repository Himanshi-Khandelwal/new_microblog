from . import api
from flask import Flask,render_template, redirect, request, url_for,session,escape
# from .form import User
#import MySQLdb
#from db_connect import connection
from functools import wraps
from config import config
from flask_oauth import OAuth

#import config
from flask_login import current_user
from app.models import signup,post_data
from app import db

GOOGLE_CLIENT_ID = '454289862376-ue1c1285rcpg0bsv837unipumimaurg0.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '_ymiPkiaMnws2o6x19cQrNx2'

REDIRECT_URI = '/oauth2callback'

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


@api.route('/')
def home():
  return render_template("main.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('api.login'))
    return decorated_function




#@app.route('/')
#def index():
#    access_token = session.get('access_token')
#    if access_token is None:
#        return redirect(url_for('api.login'))

#    access_token = access_token[0]
#    from urllib2 import Request, urlopen, URLError

#    headers = {'Authorization': 'OAuth '+access_token}
#    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
#                  None, headers)
#    try:
#        res = urlopen(req)
#    except URLError, e:
#        if e.code == 401:
#            # Unauthorized - bad token
#            session.pop('access_token', None)
#            return redirect(url_for('api.login'))
#        return res.read()

#    return res.read()

@app.route('/signin')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('api.login'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')









@api.route('/welcome/<username>')
def welcome(username):
 return render_template("welcome.html")

@api.route('/post/<username>',methods=['GET','POST'])
@login_required
def post(username):
    if request.method =='POST':
        post_d = post_data()
        post_d.post = request.form['post']
        post_d.title = request.form['title']
        post_d.tag = request.form['tag']
        post_d.post_id = session['user_id']
        db.session.add(post_d)
        db.session.commit()
    return render_template("post.html",username=username)

@api.route("/login/", methods=['POST','GET'])
def login():
    if request.method =='POST':
               username = request.form['username']

               password = request.form['password']
               #print password, username

               user = signup.query.filter_by(username=username).first()
               #print user.password
               if user!=None:
                   if user.password == password:
                        #print "yooo"
                        session['logged_in']=username
                        session['user_id']=user.id
                        return redirect(url_for('api.post',username=user.username))
                   else:
                        #print "NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
                        pass
               else:
		   return redirect(url_for('api.sign_up'))
    return render_template('login.html')


@api.route('/signup/',methods=['GET','POST'])
def sign_up():
    error=None
    if request.method == 'POST':
        user = signup()
        user.username = request.form['username']
        user.email = request.form['email']
        user. password = request.form['password']
        user.mobile = request.form['mobile']
        if signup.query.filter_by(username=user.username).first():
            error="Username Already exists"
        else:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('api.post',username = user.username))
    return render_template("signup.html",error=error)


# @app.route('/search/', methods = ['POST','GET'])
# @login_required
# def search():
#     print "done"
#     error=None
#     results=None
#     if request.method == 'POST':
#         print "coming"
#         title = request.form['search']
#         results = post_data.query.filter_by(title = title, post_id = session['user_id'])
#         feed = post_data.query.all()
#         if results != None:
#             print "doing"
#             return render_template('show-search.html', title=results.title,feed=feed)
#         #    return redirect(url_for('show-search',title=results.title))
#         else:
# 			error = "No Post Related to this Title"
#     return redirect(url_for('show_title',error=error))
#     #return render_template('post.html', error=error)
#
# @app.route("/show_title/<error>")
# @login_required
# def show_title(error):
# 	return render_template('show-search.html', error=error)

@api.route('/search/', methods = ['POST','GET'])
def search():
    results=None
    if request.method == 'POST':
        keyword = request.form['search']
        results = post_data.query.filter_by(title = keyword )#, post_id = session['user_id'])

    return render_template('search.html', results=results)


@api.route('/all_posts/')
def show_post():
    all_posts = post_data.query.filter_by(post_id= session['user_id'])
    return render_template('show.html', all_posts=all_posts)


@api.route("/user/<username>")
@login_required
def user(username):
    return render_template('user.html',username=username)

@api.route('/delete/<title>', methods=['POST'])
def delete_entry(title):
    results=None
    if title == "":
        keyword = request.form['delete']
    else:
        keyword = title
    results = post_data.query.filter_by(title = keyword ,post_id= session['user_id']).delete()
    db.session.commit()
    all_posts = post_data.query.filter_by(post_id= session['user_id'])
    return render_template('show.html', all_posts=all_posts)


@api.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('api.login'))
