# app/__init__.py

import os
from flask import Flask, Blueprint, render_template
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS

# local imports
from config import config
from .my_api.v1.parties import CreateParty, GetAllParties, PartyById
from .my_api.v1.offices import CreateOffice, GetAllOffices, OfficeById
from .my_api.v2.auth import RegisterUser, LoginUser, ConfirmUser, ResetPassword
from .my_api.v2.vote import RegisterCandidate, CastVote, GetVotes, FilePetition
from .my_api.v2.party import CreatePartyV2, GetPartiesV2, EditPartyV2
from .my_api.v2.office import CreateOfficeV2, GetOfficesV2, GetOfficeByIdV2
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
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '5693f3b210d6f4'
    app.config['MAIL_PASSWORD'] = 'ec0603fcb53a52'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    app.register_blueprint(v1, url_prefix='/api/v1')
    app.register_blueprint(v2, url_prefix='/api/v2')

    database_init()

    # heroku landing
    @app.route('/')
    def heroku():
        return render_template('index.html')

    JWTManager(app)

    Mail(app)

    CORS(app)

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
api_v2.add_resource(GetVotes, '/vote/<int:office_serial>')
api_v2.add_resource(FilePetition, '/vote/petition')
api_v2.add_resource(ResetPassword, '/auth/resetpassword')
api_v2.add_resource(CreatePartyV2, '/parties')
api_v2.add_resource(GetPartiesV2, '/parties')
api_v2.add_resource(EditPartyV2, '/parties/<int:party_id>')
api_v2.add_resource(CreateOfficeV2, '/offices')
api_v2.add_resource(GetOfficesV2, '/offices')
api_v2.add_resource(GetOfficeByIdV2, '/offices/<int:office_id>')
api_v2.add_resource(ConfirmUser, '/confirmuser/<token>')
