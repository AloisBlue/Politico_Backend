# vote.py
# imports
from flask_restful import Resource, reqparse
import psycopg2
import datetime
from flask_jwt_extended import (jwt_required, get_jwt_identity)

# local imports
from ..database import database

connection = database()
cur = connection.cursor()


class RegisterCandidate(Resource):
    """docstring for RegisterCandidate."""
    parser = reqparse.RequestParser()
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

    @jwt_required
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
        office = data['office']
        party = data['party']
        # validations
        while True:
            if not office:
                return {'Message': 'Office is empty'}, 400
            elif not party:
                return {'Message': 'Party is empty'}, 400
            else:
                break
        try:
            # get user's details
            current_user = get_jwt_identity()
            cur.execute("SELECT user_id, firstname, lastname FROM Users WHERE email=%(current_user)s;", {
                'current_user': current_user
            })
            result = cur.fetchone()
            user_id = result[0]
            firstname = result[1]
            lastname = result[2]
            # check if user_id has registered already
            cur.execute("SELECT * FROM Candidates WHERE user_id=%(user_id)s;", {
                'user_id': user_id
            })
            user_id_exist = cur.fetchone()
            if user_id_exist is None:
                # register candidate
                cur.execute("INSERT INTO Candidates(firstname, lastname, office, party, user_id) VALUES(%(firstname)s, %(lastname)s, %(office)s, %(party)s, %(user_id)s);", {
                    'firstname': firstname, 'lastname': lastname, 'office': data['office'], 'party': data['party'], 'user_id': user_id
                })
                connection.commit()
                return {'Message': 'Candidate {} registered to vie for office of the {}.'.format(firstname, office), 'Details': data}, 201
            else:
                return {"Message": "You have already registered as a candidate for {}.".format(office)}
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

    @jwt_required
    def post(self):
        cur.execute(
            """CREATE TABLE if not EXISTS Petitions(
            petition_id serial PRIMARY KEY,
            petition_date TIMESTAMP,
            user_id int,
            created_by varchar (50) NOT NULL,
            office varchar (50) NOT NULL,
            body varchar (100) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id));"""
        )
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
            # get user_id
            current_user = get_jwt_identity()
            cur.execute("SELECT user_id FROM Users WHERE email=%(current_user)s;", {
                'current_user': current_user
            })
            result = cur.fetchone()
            user_id = result[0]
            cur.execute("SELECT * FROM Votes WHERE user_id=%(user_id)s;", {
                'user_id': user_id
            })
            user_voted = cur.fetchone()
            cast_date = datetime.datetime.utcnow()
            if user_voted is None:
                cur.execute("INSERT INTO Votes(user_id, cast_date, president, governor, mca) VALUES(%(user_id)s, %(cast_date)s, %(president)s, %(governor)s, %(mca)s);", {
                    'user_id': user_id, 'cast_date': cast_date, 'president': president, 'governor': governor, 'mca': mca
                    })
                connection.commit()
                return {'Message': 'Vote casted!!!'}, 200
            else:
                return {'Message': 'You have already voted'}, 403
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class GetVotes(Resource):
    """docstring for GetVotes."""
    @jwt_required
    def get(self, office_serial):
        try:
            # get presidents
            cur.execute("SELECT president FROM Votes;")
            president = {
                "President's Office Results": cur.fetchall()
            }
            # get governor
            cur.execute("SELECT governor FROM Votes;")
            governor = {
                "Governor's Office Results": cur.fetchall()
            }
            # get mca
            cur.execute("SELECT mca FROM Votes;")
            mca = {
                "Mca's Office Results": cur.fetchall()
            }
            # office serials
            # 1 for president
            # 2 for governor
            # 3 for mca
            if office_serial == 1:
                return {'Message': president}, 200
            elif office_serial == 2:
                return {'Message': governor}, 200
            elif office_serial == 3:
                return {'Message': mca}, 200
            else:
                return {'Message': 'Sorry, no office registered under that serial'}, 404
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class FilePetition(Resource):
    """docstring for FilePetition."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'body',
        type=str,
        required=True,
        help="Body description required"
    )

    @jwt_required
    def post(self):
        data = FilePetition.parser.parse_args()
        body = data['body']
        petition_date = datetime.datetime.utcnow()
        current_user = get_jwt_identity()
        # get user details
        cur.execute("SELECT user_id, firstname FROM Users WHERE email=%(current_user)s;", {
            'current_user': current_user
        })
        result = cur.fetchone()
        user_id = result[0]
        created_by = result[1]
        cur.execute("SELECT office FROM Candidates WHERE user_id=%(user_id)s;", {
            'user_id': user_id
        })
        result2 = cur.fetchone()
        office = result2[0]
        cur.execute("INSERT INTO Petitions(petition_date, user_id, created_by, office, body) VALUES(%(petition_date)s, %(user_id)s, %(created_by)s, %(office)s, %(body)s);", {
                'petition_date': petition_date, 'user_id': user_id, 'created_by': created_by, 'office': office, 'body': body
                })
        connection.commit()
        return {'Message': 'Your petition is received and recorded'}, 200
