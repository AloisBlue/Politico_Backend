# app/my_api/v2/auth.py
# imports
from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
import psycopg2
import validators
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

# local imports
from ..database import database

connection = database()
cur = connection.cursor()


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
        cur.execute(
                """CREATE TABLE if not EXISTS Candidates(
                   candidate_id serial PRIMARY KEY,
                   firstname varchar (50) NOT NULL,
                   lastname varchar (50) NOT NULL,
                   office varchar (50) NOT NULL,
                   party varchar (50) NOT NULL,
                   user_id int,
                   FOREIGN KEY (user_id) REFERENCES users(user_id)
                   );""")
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
        # validations
        while True:
            if not email:
                return {'Message': 'Email cannot be empty'}, 400
            elif not firstname:
                return {'Message': 'Firstname cannot be empty'}, 400
            elif not lastname:
                return {'Message': 'Lastname cannot be empty'}, 400
            elif not othername:
                return {'Message': 'Othername cannot be empty'}, 400
            elif not phonenumber:
                return {'Message': 'You must provide a phone number'}, 400
            elif not passporturl:
                return {'Message': 'Passport url is needed'}, 400
            elif not password:
                return {'Message': 'Password is empty'}, 400
            elif not passwordconfirm:
                return {'Message': 'Password confirm is empty'}, 400
            elif len(password) < 8:
                return {'Message': 'Password should have minimum of 8 characters'}, 400
            elif password != passwordconfirm:
                return {'Message': 'Passwords must match'}, 400
            elif not validators.email(email):
                return {'Message': 'Email format not correct'}, 400
            elif not validators.url(passporturl):
                return {'Message': 'The passport URL is invalid'}, 400
            else:
                break

        password_hash = Bcrypt().generate_password_hash(password).decode()
        try:
            cur.execute("SELECT * FROM Users WHERE email = %(email)s",
                        {'email': data['email']})
            # check whether user exists
            user_exists = cur.fetchone()
            if user_exists is not None:
                return {'Message': 'User with such email already exists.'}, 400
            cur.execute("INSERT INTO Users(email, firstname, lastname, othername, phonenumber, passporturl, password_hash, isadmin) VALUES(%(email)s, %(firstname)s, %(lastname)s, %(othername)s, %(phonenumber)s, %(passporturl)s, %(password_hash)s, %(isadmin)s);", {
                'email': data['email'], 'firstname': data['firstname'], 'lastname': data['lastname'], 'othername': data['othername'], 'phonenumber': data['phonenumber'], 'passporturl': data['passporturl'], 'password_hash': password_hash, 'isadmin': isAdmin
            })
            connection.commit()
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return {'Message': 'Account for {} was succesfully created!!!'.format(firstname),
                    'Access Token': access_token}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class LoginUser(Resource):
    """docstring for LoginUser."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email address required"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
    )

    def post(self):
        data = LoginUser.parser.parse_args()
        email = data['email']
        password = data['password']
        # validations
        while True:
            if not email:
                return {'Message': 'You must provide an email'}, 400
            elif not password:
                return {'Message': 'You must provide a password'}, 400
            elif not validators.email(email):
                return {'Message', 'Email format is invalid'}, 400
            else:
                break
        # login
        try:
            cur.execute("SELECT password_hash FROM Users WHERE email = %(email)s", {
                'email': data['email']
            })
            # check if email exists
            result = cur.fetchone()
            user_exists = result[0]
            if Bcrypt().check_password_hash(user_exists, password):
                access_token = create_access_token(identity=email)
                refresh_token = create_refresh_token(identity=email)
                return {'Message': 'Logged in as {}'.format(email),
                        'Access Token': access_token}, 200
            else:
                return {'Message': 'Invalid credentials'}, 403

        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class ResetPassword(Resource):
    """docstring for ResetPassword."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email field empty"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password field empty"
    )
    parser.add_argument(
        'passwordconfirm',
        type=str,
        required=True,
        help="Confirm password field empty"
    )

    def put(self):
        data = ResetPassword.parser.parse_args()
        email = data['email']
        password = data['password']
        passwordconfirm = data['passwordconfirm']
        while True:
            if not email:
                return {'Message': 'Email cannot be empty'}, 400
            elif not password:
                return {'Message': 'Password cannot be empty'}, 400
            elif not passwordconfirm:
                return {'Message': 'Confirm password cannot be empty'}, 400
            else:
                break
        password_hash = Bcrypt().generate_password_hash(password).decode()
        cur.execute("UPDATE Users SET password_hash = %(password_hash)s WHERE email = %(email)s", {
            'password_hash': password_hash, 'email': email
        })
        connection.commit()
        return {'Message': 'Password reset was successful'}, 200
