import os
from app import create_app
from flask_script import Manager
from app import db

app = create_app('default')

manager = Manager(app)

@manager.command
def initdb():
    db.drop_all(bind=None)
    db.create_all(bind=None)

if __name__ == '__main__':
	manager.run()