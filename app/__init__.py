# app/__init__.py

import os
from flask import Flask, Blueprint, render_template
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# local imports
from config import config
from .my_api.v1.parties import CreateParty, GetAllParties, PartyById
from .my_api.v1.offices import CreateOffice, GetAllOffices, OfficeById
from .my_api.v2.auth import RegisterUser, LoginUser
from .my_api.v2.vote import RegisterCandidate, CastVote
from.my_api.database import database_init

v1 = Blueprint('api', __name__)
api = Api(v1)

v2 = Blueprint('api_v2', __name__)
api_v2 = Api(v2)


# Initialize the app
def create_app(config_value):
    app = Flask(__name__, instance_relative_config=True)

    # Config file
    app.config.from_object(config[config_value])
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.register_blueprint(v1, url_prefix='/api/v1')
    app.register_blueprint(v2, url_prefix='/api/v2')

    database_init()

    # heroku landing
    @app.route('/')
    def heroku():
        return render_template('index.html')

    JWTManager(app)

    load_dotenv()

    return app


# Add resource
api.add_resource(CreateParty, '/parties')
api.add_resource(GetAllParties, '/parties')
api.add_resource(PartyById, '/parties/<int:party_id>')
api.add_resource(CreateOffice, '/offices')
api.add_resource(GetAllOffices, '/offices')
api.add_resource(OfficeById, '/offices/<int:office_id>')
api_v2.add_resource(RegisterUser, '/auth/signup')
api_v2.add_resource(LoginUser, '/auth/login')
api_v2.add_resource(RegisterCandidate, '/vote/candidate')
api_v2.add_resource(CastVote, '/vote')
