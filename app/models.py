from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()


class signup(db.Model):
  __tablename__ = 'signup'
  user_id=db.Column(db.Integer,primary_key=True,nullable=True)
  username=db.Column(db.String(100), primary_key=True)
  email=db.Column(db.String(100), unique=True)
  password=db.Column(db.String(100),unique=True)
  mobile=db.Column(db.Integer, unique=True)


  def __init__(self,username,email,password,mobile):
        self.username = username
        self.email=email
        self.password = password
        self.mobile=mobile

class post_data(db.Model):
    __tablename__ = 'post_data'
    id=db.Column(db.Integer,primary_key=True)
    post=db.Column(db.String(1000))
    title=db.Column(db.String(50))
    tag=db.Column(db.String(50))
    post_id=db.Column(db.Integer)

    def __init__(self,post,title,tag,post_id):
          self.post=post
          self.title=title
          self.tag=tag
          self.post_id=post_id
