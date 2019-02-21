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
        'user_id',
        type=str,
        required=True,
        help="User id required"
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
        user_id = data['user_id']
        # validations
        while True:
            if not office:
                return {'Message': 'Office is empty'}, 400
            elif not party:
                return {'Message': 'Party is empty'}, 400
            elif not user_id:
                return {'Message': 'user_id is empty'}, 400
            else:
                break
        try:
            # get user's details
            current_user = get_jwt_identity()
            cur.execute("SELECT isadmin FROM Users WHERE email = %(email)s;", {
                'email': current_user
            })
            user_exists = cur.fetchone()
            is_admin = user_exists[0]
            if is_admin:
                cur.execute("SELECT firstname, lastname FROM Users WHERE user_id=%(user_id)s;", {
                    'user_id': user_id
                })
                result = cur.fetchone()
                firstname = result[0]
                lastname = result[1]
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
                    return {
                        'status': 201,
                        'Message': 'Candidate {} registered to vie for office of the {}.'.format(firstname, office), 'data': data}, 201
                else:
                    return {
                        'status': 409,
                        "Message": "You have already registered the candidate."}, 409
            else:
                return {
                    'status': 403,
                    'Message': 'Adminstrators only'
                }, 403
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
                return {
                    'status': 201,
                    'Message': 'Vote casted!!!',
                    'data': data}, 200
            else:
                return {
                    'status': 409,
                    'Message': 'You have already voted'}, 409
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
            p_results = cur.fetchall()
            president = {
                "President's Office Results": p_results
            }
            # get governor
            cur.execute("SELECT governor FROM Votes;")
            g_results = cur.fetchall()
            governor = {
                "Governor's Office Results": g_results
            }
            # get mca
            cur.execute("SELECT mca FROM Votes;")
            m_results = cur.fetchall()
            mca = {
                "Mca's Office Results": m_results
            }
            # office serials
            # 1 for president
            # 2 for governor
            # 3 for mca
            print(type(p_results))
            if office_serial == 1:
                return {
                    'status': 200,
                    'Data': president,
                    'votes': len(p_results)}, 200
            elif office_serial == 2:
                return {
                    'status': 200,
                    'Data': governor,
                    'votes': len(g_results)}, 200
            elif office_serial == 3:
                return {
                    'status': 200,
                    'Data': mca,
                    'votes': len(m_results)}, 200
            else:
                return {
                    'status': 404,
                    'Message': 'Sorry, no office registered under that serial'}, 404
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
        cur.execute("SELECT * FROM Petitions WHERE user_id=%(user_id)s;", {
            'user_id': user_id
        })
        user_petitioned = cur.fetchone()
        if user_petitioned is None:
            cur.execute("INSERT INTO Petitions(petition_date, user_id, created_by, office, body) VALUES(%(petition_date)s, %(user_id)s, %(created_by)s, %(office)s, %(body)s);", {
                    'petition_date': petition_date, 'user_id': user_id, 'created_by': created_by, 'office': office, 'body': body
                })
            connection.commit()
            return {
                'status': 201,
                'Message': 'Your petition is received and recorded',
                'createBy': user_id,
                'data': data}, 201
        else:
            return {
                'status': 409,
                'Message': 'You have already filed a petition'}, 409
