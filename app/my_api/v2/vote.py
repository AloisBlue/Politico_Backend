# vote.py
# imports
from flask_restful import Resource, reqparse
import psycopg2
import datetime

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
        cur.execute(
            """CREATE TABLE if not EXISTS Votes(
            vote_id serial PRIMARY KEY,
            user_id INT,
            cast_date TIMESTAMP,
            president varchar (50) NOT NULL,
            governor varchar (50) NOT NULL,
            mca varchar (50) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id));"""
        )
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


class CastVote(Resource):
    """docstring for CastVote."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'president',
        type=str,
        required=True,
        help="President not selected"
    )
    parser.add_argument(
        'governor',
        type=str,
        required=True,
        help="Governor not selected"
    )
    parser.add_argument(
        'mca',
        type=str,
        required=True,
        help="Mca not selected"
    )

    def post(self):
        data = CastVote.parser.parse_args()
        president = data['president']
        governor = data['governor']
        mca = data['mca']
        # validations
        while True:
            if not president:
                return {'Message': 'President option empty'}, 400
            elif not governor:
                return {'Message': 'Governor option empty'}, 400
            elif not mca:
                return {'Message': 'Mca option empty'}, 400
            else:
                break
        try:
            # sample user_id
            user_id = 1
            cast_date = datetime.datetime.utcnow()
            cur.execute("INSERT INTO Votes(user_id, cast_date, president, governor, mca) VALUES(%(user_id)s, %(cast_date)s, %(president)s, %(governor)s, %(mca)s);", {
                'user_id': user_id, 'cast_date': cast_date, 'president': president, 'governor': governor, 'mca': mca
            })
            connection.commit()
            return {'Message': 'Vote casted!!!'}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
