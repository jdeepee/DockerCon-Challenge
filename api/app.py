from flask import Flask, render_template, flash, request, url_for, redirect, session, send_file, Response, jsonify, abort
from flask_restful import Resource, Api 

application = Flask(__name__) #Creating application
api = Api(application) #Creating API

#Import our database model
from models.database_model import *

db.init_app(application)
Session = sessionmaker()
Session.configure(bind=engine)

#Initialise the database session
session = Session()
session._model_changes = {}

#Importing our classes
from rest.index import *
from rest.controllers import * 
from rest.devices import * 

#Routes
api.add_resource(Index, '/')
api.add_resource(Controllers, '/controllers/')
api.add_resource(ControllersDevices, '/controllers/<id>/devices/')
api.add_resource(ControllersDevice, '/controllers/<id>/devices/<id2>/')