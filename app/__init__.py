#app/__init__.py

from flask import Flask, Blueprint
from flask_restful import Resource, Api

v1 = Blueprint('api', __name__)
api = Api(v1)

#local imports
from config import config

# Hello world function testing
class HelloWorld(Resource):
	"""docstring for HelloWorld"""
	def get(self):
		return ("Hello")

# Initialize the app
def create_app(config_value):
    app = Flask(__name__, instance_relative_config=True)

    #Config file
    app.config.from_object(config[config_value])

    app.register_blueprint(v1)

    return app

#Add resource
api.add_resource(HelloWorld, '/')
