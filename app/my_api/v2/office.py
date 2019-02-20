from flask_restful import Resource, reqparse
import validators
import psycopg2
from flask_jwt_extended import (jwt_required, get_jwt_identity)

# local imports
from ..database import database

connection = database()
cur = connection.cursor()


class CreateOfficeV2(Resource):
    """docstring for CreateOfficeV2."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name of the office should be filled"
    )
    parser.add_argument(
        'type',
        type=str,
        required=True,
        help="Type of the office should be filled"
    )

    @jwt_required
    def post(self):
        data = CreateOfficeV2.parser.parse_args()
        name = ['name']
        type = ['type']
        # validation
        while True:
            if not name or not type:
                return {'Message': 'Check for empty fields'}
            elif len(data['name']) < 3 or len(data['name']) > 15:
                return {'Message': 'Name must be between 3 and 15 characters'}
            elif len(data['type']) < 3 or len(data['type']) > 20:
                return {'Message': 'Office type description must be between 3 and 20 characters'}
            else:
                break

        try:
            # check if user is admin
            current_user = get_jwt_identity()
            cur.execute("SELECT isadmin FROM Users WHERE email = %(email)s;", {
                'email': current_user
            })
            user_exists = cur.fetchone()
            is_admin = user_exists[0]
            if is_admin:
                # check if office is registered
                cur.execute("SELECT * FROM Offices WHERE name = %(name)s;", {
                    'name': data['name']
                })
                office_exist = cur.fetchone()
                if office_exist is None:
                    cur.execute("INSERT INTO Offices(name, type) VALUES(%(name)s, %(type)s);", {
                        'name': data['name'], 'type': data['type']
                    })
                    connection.commit()
                    return {
                        'status': 201,
                        'Message': 'Office successfully added',
                        'data': data}, 201
                return {
                    'status': 409,
                    'Message': 'The office already exists'}, 409
            else:
                return {
                    'status': 403,
                    'Message': 'This panel is for administrators only'}, 403
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class GetOfficesV2(Resource):
    """docstring for GetOfficesV2."""
    @jwt_required
    def get(self):
        try:
            cur.execute("SELECT * FROM Offices;")
            offices = cur.fetchall()
            return {
                'status': 200,
                'Message': 'This includes offices available',
                'data': offices}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class GetOfficeByIdV2(Resource):
    """docstring for EditPartyV2."""
    @jwt_required
    def get(self, office_id):
        try:
            cur.execute("SELECT * FROM Offices WHERE office_id = %s", [office_id])
            office = cur.fetchall()
            return {
                'status': 200,
                'Message': 'This are the party details',
                'data': office}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
