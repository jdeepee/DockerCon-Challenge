from flask_restful import Resource

class Index(Resource):
	def get(self):
		return Response(response='API for controlling the world', status=200, mimetype='text/plain')