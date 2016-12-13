from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint)

	db.init_app(app)

	return app

"""	
app=Flask(__name__)
#app.config.from_object ('config')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:codecode@localhost/tutorials'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
#app.secret_key = SECRET_KEY
db=SQLAlchemy(app)
#db.init_app(login)
from app import views
"""