from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session
from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..app import *

engine = create_engine("postgresql://josh:josh12345678@aa169kxdyt8mkhx.ciy2qyqwn3ta.us-west-1.rds.amazonaws.com/api")
db = SQLAlchemy(application)

Base = declarative_base()

class Controller(db.Model):
	__tablename__ = "controllers"

	id = db.Column('id', db.Unicode, primary_key=True)

	def __repr__(self):
		return "<Controller(id='%s')>" % (self.id)

class Device(db.Model):
	__tablename__ = "devices"

	id = db.Column('id', db.Unicode, primary_key=True)
	state = db.Column('state', db.Integer)
	max_state = db.Column('max_state', db.Integer)
	parent_controller = db.Column('controller', db.Unicode, db.ForeignKey('controllers.id'))

	controller = db.relationship('Controller', foreign_keys=parent_controller)