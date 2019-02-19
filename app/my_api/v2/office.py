from flask_restful import Resource, reqparse
import validators
import psycopg2

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

    @classmethod
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
            cur.execute("INSERT INTO Offices(name, type) VALUES(%(name)s, %(type)s);", {
                'name': data['name'], 'type': data['type']
            })
            connection.commit()
            return {'Message': 'Offie added'}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class GetOfficesV2(Resource):
    """docstring for GetOfficesV2."""
    def get(self):
        try:
            cur.execute("SELECT * FROM Offices;")
            offices = cur.fetchall()
            return {'Message': offices}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
