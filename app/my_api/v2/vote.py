# vote.py
# imports
from flask_restful import Resource, reqparse
import psycopg2

# local imports
from ..database import database

connection = database()
cur = connection.cursor()


class RegisterCandidate(Resource):
    """docstring for RegisterCandidate."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'firstname',
        type=str,
        required=True,
        help="Firstname name required"
    )
    parser.add_argument(
        'lastname',
        type=str,
        required=True,
        help="Lastname is required"
    )
    parser.add_argument(
        'office',
        type=str,
        required=True,
        help="Office is required"
    )
    parser.add_argument(
        'party',
        type=str,
        required=True,
        help="Party is required"
    )

    def post(self):
        data = RegisterCandidate.parser.parse_args()
        firstname = data['firstname']
        lastname = data['lastname']
        office = data['office']
        party = data['party']
        # validations
        while True:
            if not firstname:
                return {'Message': 'Firstname is empty'}, 400
            elif not lastname:
                return {'Message': 'Lastname is empty'}, 400
            elif not office:
                return {'Message': 'Office is empty'}, 400
            elif not party:
                return {'Message': 'Party is empty'}, 400
            else:
                break
        try:
            # cur.execute("SELECT user_id from Candidates WHERE user_id = %(user_id)s", {
            #    'user_id': user_id
            # })
            # demo user_id
            user_id = 1
            cur.execute("INSERT INTO Candidates(firstname, lastname, office, party, user_id) VALUES(%(firstname)s, %(lastname)s, %(office)s, %(party)s, %(user_id)s);", {
                'firstname': data['firstname'], 'lastname': data['lastname'], 'office': data['office'], 'party': data['party'], 'user_id': user_id
            })
            connection.commit()
            return {'Message': 'Candidate {} registered to vie for office of the {}.'.format(firstname, office), 'Details': data}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
