from flask_restful import Resource
from flask import Flask, render_template, flash, request, url_for, redirect, session, send_file, Response, jsonify, abort
from ..app import *

class Controllers(Resource):
	def get(self):
		query = db.session.query(Controller).all()
		db.session.close()

		if query is not None:
			response = ""

			for controller in query:
				response += controller.id + ","

			return Response(response=response, status=200, mimetype='text/plain')

		else:
			return Response(response='you have no controllers', status=400, mimetype='text/plain')

	def post(self):
		id = request.args.get('id')

		check = db.session.query(Controller).filter(Controller.id == id).first()

		if check is None:
			try:
				data = Controller(id=id)
				db.session.add(data)
				db.session.commit()

			except:
				db.session.rollback()
				return Response(response='Something on the API went wrong', status=400, mimetype='text/plain')
				raise

			finally:
				db.session.close()

			return Response(response='id:'+id, status=200, mimetype='text/plain')

		else:
			return Response(response='That controller ID already exsists', status=400, mimetype='text/plain')