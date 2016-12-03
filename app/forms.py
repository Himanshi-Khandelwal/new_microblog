from flask_wtf import Form
from wtforms import StringField, DateTimeField,PasswordField, IntegerField
from wtforms validators import DataRequired

class login(Form):
    username=StringField("username",validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class post_data(Form):
    id=IntegerField("id",validators=[DataRequired()])
    post=StringField("post",validators=[DataRequired()])
    date_time=DateTimeField("date_time",validators=[DataRequired()])
    title=StringField("title",validators=[DataRequired()])
    tag=StringField("tag",validators=[DataRequired()])
