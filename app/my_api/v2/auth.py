# app/my_api/v2/auth.py
# imports
from flask_restful import Resource, reqparse
import psycopg2
import bcrypt
import validators

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
            elif not  passwordconfirm:
                return {'Message': 'Password confirm is empty'}, 400
            elif len(password) < 8:
                return {'Message': 'Password should have minimum of 8 characters'}, 400
            elif password != passwordconfirm:
                return {'Message': 'Passwords must match'}, 400
            elif not validators.email(email):
                return {'Message': 'Email format not correct'}, 400
            elif not validators.url(passporturl):
                return {'Message': 'Passport URL is invalid'}
            else:
                break

        password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
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
            return {'Message': 'Account for {} was succesfully created!!!'.format(data['firstname'])}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
