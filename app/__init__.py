from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db
from config import SECRET_KEY
from flask_oauth import OAuth

app=Flask(__name__)
#app.config.from_object ('config')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:himanshi@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
DEBUG=True
app.secret_key = SECRET_KEY
app.debug = DEBUG
oauth = OAuth()
db=SQLAlchemy(app)
#db.init_app(login)
from app import views
