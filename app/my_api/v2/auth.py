# app/my_api/v2/auth.py
# imports
from flask_restful import Resource, reqparse
import psycopg2
import bcrypt

# local imports
from ..database import database


class RegisterUser(Resource):
    """docstring for RegisterUser."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email is required"
    )
    parser.add_argument(
        'firstname',
        type=str,
        required=True,
        help="Firstname is required"
    )
    parser.add_argument(
        'lastname',
        type=str,
        required=True,
        help="Lastname is required"
    )
    parser.add_argument(
        'othername',
        type=str,
        required=True,
        help="Othername is required"
    )
    parser.add_argument(
        'phonenumber',
        type=str,
        required=True,
        help="Phone number is required"
    )
    parser.add_argument(
        'passporturl',
        type=str,
        required=True,
        help="Passport URL is required"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
    )
    parser.add_argument(
        'passwordconfirm',
        type=str,
        required=True,
        help="Confirm password is required"
    )

    def post(self):
        connection = database()
        cur = connection.cursor()
        data = RegisterUser.parser.parse_args()
        email = data['email']
        firstname = data['firstname']
        lastname = data['lastname']
        othername = data['othername']
        phonenumber = data['phonenumber']
        passporturl = data['passporturl']
        password = data['password']
        passwordconfirm = data['passwordconfirm']
        isAdmin = False
        while False:
            if email:
                return {'Message': 'Email is empty'}, 400
            elif firstname:
                return {'Message': 'Firstname is empty'}, 400
            elif lastname:
                return {'Message': 'Lastname is empty'}, 400
            elif othername:
                return {'Message': 'Other name is empty'}, 400
            elif phonenumber:
                return {'Message': 'Phone number is empty'}, 400
            elif passporturl:
                return {'Message': 'Passport URL is empty'}, 400
            elif password:
                return {'Message': 'Password is empty'}, 400
            elif passwordconfirm:
                return {'Message': 'Password confirm is empty'}, 400
            else:
                break

        password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        try:
            cur.execute("SELECT * FROM Users WHERE email = %(email)s",
                        {'email': data['email']})
            # check whether user exists
            user_exists = cur.fetchone()
            if user_exists is not None:
                return {'Message': 'Email already exists'}, 400
            cur.execute("INSERT INTO Users(email, firstname, lastname, othername, phonenumber, passporturl, password_hash, isadmin) VALUES(%(email)s, %(firstname)s, %(lastname)s, %(othername)s, %(phonenumber)s, %(passporturl)s, %(password_hash)s, %(isadmin)s);", {
                'email': data['email'], 'firstname': data['firstname'], 'lastname': data['lastname'], 'othername': data['othername'], 'phonenumber': data['phonenumber'], 'passporturl': data['passporturl'], 'password_hash': password_hash, 'isadmin': isAdmin
            })
            connection.commit()
            return {'Message': 'Your account was successfully created'}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
