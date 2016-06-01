from flask_restful import Resource
from ..app import *

class ControllersDevices(Resource):
	def get(self, id):
		query = db.session.query(Controller, Device).join(Device).filter(Controller.id == id, Device.parent_controller == id).all()
		db.session.close()

		if query is not None:
			response = ""

			for c, d in query:
				response += d.id+":"+d.state

			return Response(response=response, status=200, mimetype='text/plain')

		else:
			return Response(response='You have no devices associated to that controller', status=200, mimetype='text/plain')

	def post(self, id):
		device_id = request.args.get('id')
		max_state = request.args.get('max_state')

		if device_id and max_state:
			check = db.session.query(Controller).filter(Controller.id == id).first()
			check2 = db.session.query(Device).filter(Device.id == device_id).first()

			if check is not None and check2 is None:
				try:
					data = Device(id=device_id, max_state=max_state, state=0, parent_controller=id)
					db.session.add(data)
					db.session.close()

				except:
					db.session.rollback()
					return Response(response='Something on the API went wrong', status=400, mimetype='text/plain')
					raise

				finally:
					db.session.close()

				return Response(response='New device successfully added!', status=200, mimetype='application/json')

			else:
				db.session.close()
				return Response(response='', status=400, mimetype='text/plain')

		else:
			return Response(response='you are missing the device ID of which you wish to create', status=400, mimetype='text/plain')


class ControllersDevice(Resource):
	def get(self, id, id2):
		query = db.session.query(Device).filter(Device.id == id2).first()

		if query is None:
			return Response(response=str(query.state), status=200, mimetype='text/plain')

		else:
			return Response(response='No such device id', status=400, mimetype='text/plain')


	def post(self, id, id2):
		check = db.session.query(Controller).filter(Controller.id == id).first()
		check2 = db.session.query(Device).filter(Device.id == id2).first()

		if check is not None and check2 is not None:
			state = request.args.get('state')

			if state:
				try:
					db.session.query(Device).filter(Device.id == id2).update({'state': state})
					db.session.commit()

				except:
					db.session.rollback()
					return Response(response='Something went wrong on the API', status=400, mimetype='text/plain')
					raise

				finally:
					db.session.close()

				return Response(response='State successfully updated!', status=200, mimetype='text/plain')

			else:
				max_state = check2.max_state
				state = check2.state

				if state+1 > max_state:
					state = 0

				else:
					state = state+1

				try:
					db.session.query(Device).filter(Device.id == id2).update({'state': state})
					db.session.commit()

				except:
					db.session.rollback()
					return Response(response='Something went wrong with the API', status=400, mimetype='text/plain')
					raise

				finally:
					db.session.close()

				return Response(response='State successfully updated!', status=200, mimetype='text/plain')

		else:
			return Response(response='There is either no matching controller or device', status=400, mimetype='text/plain')
