from . import api
from flask import Flask,render_template, redirect, request, url_for,session,escape
# from .form import User
#import MySQLdb
#from db_connect import connection
from functools import wraps
#import config
from flask_login import current_user
from app.models import signup,post_data
from app import db


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

@api.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('api.login'))
