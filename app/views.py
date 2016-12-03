from app import app
from flask import Flask,render_template, redirect, request, url_for,session,escape
# from .form import User
#import MySQLdb
#from db_connect import connection
import config
from models import db,signup


@app.route('/')
def home():
 return render_template("main.html")



@app.route('/welcome/<username>')
def welcome(username):
 return render_template("welcome.html")



@app.route("/login/", methods=['POST','GET'])
def login():
    if request.method =='POST':
               username = request.form['username']
        #email = request.form['email']
               password = request.form['password']
               print password, username
        #mobile = request.form['mobile']
               user = signup.query.filter_by(username=username).first()
               print user.password
               if user.password == password:
                    print "yooo"
                    return redirect(url_for('welcome',username=user.username))
               else:
                    print "NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
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
            return redirect(url_for('welcome',username = user.username))
    return render_template("signup.html")



@app.route("/user/<username>")
def user(username):
    return render_template('user.html',username=username)
