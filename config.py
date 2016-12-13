import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY ='t0p s3cr3t'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://myprojectuser:password@localhost/myproject'


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://myprojectuser:password@localhost/myproject'

class ProductionConfig(Config):
	DEBUG = False
	SECRET_KEY ='t0p s3cr3t'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://myprojectuser:password@localhost/myproject'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}