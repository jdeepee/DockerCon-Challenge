from flask_restful import Resource
from flask import Flask, render_template, flash, request, url_for, redirect, session, send_file, Response, jsonify, abort

class Index(Resource):
	def get(self):
		return Response(response='API for controlling the world', status=200, mimetype='text/plain')