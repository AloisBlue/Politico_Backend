from flask_restful import Resource, reqparse
import validators
import psycopg2
from flask_jwt_extended import (jwt_required, get_jwt_identity)

# local imports
from ..database import database

connection = database()
cur = connection.cursor()


class CreatePartyV2(Resource):
    """docstring for CreateParty."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name of the party should be filled"
    )
    parser.add_argument(
        'hqaddress',
        type=str,
        required=True,
        help="Head quarter address needed"
    )
    parser.add_argument(
        'logourl',
        type=str,
        required=True,
        help="Logo url needed"
    )

    @jwt_required
    def post(self):
        data = CreatePartyV2.parser.parse_args()
        name = ['name']
        hqaddress = ['hqaddress']
        logourl = ['logourl']
        # validation
        while True:
            if not name or not hqaddress or not logourl:
                return {'Message': 'Check for empty fields'}
            elif len(data['name']) < 3 or len(data['name']) > 15:
                return {'Message': 'Name must be between 3 and 15 characters'}
            elif len(data['hqaddress']) < 3 or len(data['hqaddress']) > 20:
                return {'Message': 'Head quarter address must be between 3 and 20 characters'}
            elif not validators.url(data['logourl']):
                return {'Message': 'You must provide a valid url'}
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
                # check if exists
                cur.execute("SELECT * FROM Parties WHERE name = %(name)s;", {
                    'name': data['name']
                })
                party_exist = cur.fetchone()
                if party_exist is None:
                    cur.execute("INSERT INTO Parties(name, hqaddress, logourl) VALUES(%(name)s, %(hqaddress)s, %(logourl)s);", {
                        'name': data['name'], 'hqaddress': data['hqaddress'], 'logourl': data['logourl']
                    })
                    connection.commit()
                    return {'Message': 'Party successfully added'}, 200
                else:
                    return {'Message': 'Party already exists'}, 400
            else:
                return {'Message': 'This panel is for administrators only'}, 403
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class GetPartiesV2(Resource):
    """docstring for GetPartiesV2."""
    @jwt_required
    def get(self):
        try:
            cur.execute("SELECT * FROM Parties;")
            parties = cur.fetchall()
            return {'Message': parties}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class EditPartyV2(Resource):
    """docstring for EditPartyV2."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name is empty"
    )
    parser.add_argument(
        'hqaddress',
        type=str,
        required=True,
        help="Hq address field empty"
    )

    @classmethod
    def get(self, party_id):
        try:
            cur.execute("SELECT * FROM Parties WHERE party_id = %s", [party_id])
            party = cur.fetchall()
            return {'Message': party}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @classmethod
    def put(self, party_id):
        data = EditPartyV2.parser.parse_args()
        name = data['name']
        hqaddress = data['hqaddress']
        while True:
            if not name:
                return {'Message': 'Name cannot be empty'}, 400
            elif not hqaddress:
                return {'Message': 'Hq address cannot be empty'}, 400
            else:
                break
        try:
            cur.execute("UPDATE Parties SET name = %s, hqaddress = %s WHERE party_id = %s", (name, hqaddress, party_id))
            connection.commit()
            return {'Message': 'The party was updated'}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @classmethod
    def delete(self, party_id):
        try:
            cur.execute("DELETE FROM Parties WHERE party_id = %s;", [party_id])
            return {'Message': 'Party deleted'}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
