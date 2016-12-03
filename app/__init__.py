from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db


app=Flask(__name__)
#app.config.from_object ('config')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:himanshi@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db=SQLAlchemy(app)
#db.init_app(login)
from app import views
