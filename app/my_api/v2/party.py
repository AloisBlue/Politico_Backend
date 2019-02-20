from flask_restful import Resource, reqparse
import validators
import psycopg2

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

    @classmethod
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
            cur.execute("INSERT INTO Parties(name, hqaddress, logourl) VALUES(%(name)s, %(hqaddress)s, %(logourl)s);", {
                'name': data['name'], 'hqaddress': data['hqaddress'], 'logourl': data['logourl']
            })
            connection.commit()
            return {'Message': 'Party added'}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class GetPartiesV2(Resource):
    """docstring for GetPartiesV2."""
    def get(self):
        try:
            cur.execute("SELECT * FROM Parties;")
            parties = cur.fetchall()
            return {'Message': parties}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
