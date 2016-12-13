from sqlalchemy.orm import relationship
from . import db


class signup(db.Model):
  __tablename__ = 'signup'
  
  id = db.Column(db.Integer, primary_key = True)
  username=db.Column(db.String(100), nullable=False)
  email=db.Column(db.String(100), unique=True)
  password=db.Column(db.String(100),unique=True)
  mobile=db.Column(db.String(10), unique=True)


class post_data(db.Model):
    __tablename__ = 'post_data'
    id = db.Column(db.Integer, primary_key = True)
    post=db.Column(db.String(1000))
    title=db.Column(db.String(50))
    tag=db.Column(db.String(50))
    post_id=db.Column(db.Integer)
