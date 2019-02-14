# test auth.py
import unittest
import os
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# local imports
from ...database import database, database_init
from app import create_app


class TestAuth(unittest.TestCase):
    """docstring for TestAuth."""
    def setUp(self):
        self.app = create_app('testing')
        self.Client = self.app.test_client()
        self.url = os.getenv("DATABASE_URL")
        connection = database()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = connection.cursor()
        # signup variables
        self.user_signs = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.sign_bad_email_format = {
            "email": "aloismburu.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.password_less = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "pasord",
            "passwordConfirm": "password"
        }
        self.password_match = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "pagaword"
        }
        self.empty_email = {
            "email": "",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.empty_firstname = {
            "email": "aloismburu@gmail.com",
            "firstname": "",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.empty_lastname = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.empty_othername = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.empty_phonenumber = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.empty_passport_url = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "",
            "password": "password",
            "passwordConfirm": "password"
        }
        self.empty_password = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "",
            "passwordConfirm": "password"
        }
        self.empty_password_confirm = {
            "email": "aloismburu@gmail.com",
            "firstname": "Alois",
            "lastname": "Blue",
            "othername": "Success",
            "phoneNumber": "0778082345",
            "passportUrl": "jdkjfld.com",
            "password": "password",
            "passwordConfirm": ""
        }

        # login variables
        self.login = {
            "email": "aloismburu@gmail.com",
            "password": "password"
        }
        self.bad_email_format = {
            "email": "aloismburu.com",
            "password": "password"
        }
        self.invalid_credentials = {
            "email": "aloismburu@gmail.com",
            "password": "pasdkld"
        }
        self.login_empty_email = {
            "email": "",
            "password": "password"
        }
        self.login_empty_password = {
            "email": "aloismburu@gmail.com",
            "password": ""
        }

        with self.app.app_context():
            # init db creating tables
            database_init()

    # user signs up
    def test_user_signsup(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.user_signs),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Account for Alois was succesfully created!!!")
        self.assertEqual(201, response.status_code)

    def test_user_exists(self):
        resp = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.user_signs),
                                    content_type='application/json')
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.user_signs),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "User with such email already exists.")
        self.assertEqual(400, response.status_code)

    def test_bad_email_format(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.sign_bad_email_format),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Email format not correct")
        self.assertEqual(400, response.status_code)

    def test_password_lessthan_8(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.password_less),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Password should have minimum of 8 characters")
        self.assertEqual(400, response.status_code)

    def test_password_match(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.password_match),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Passwords must match")
        self.assertEqual(400, response.status_code)

    def test_empty_email(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_email),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Email cannot be empty")
        self.assertEqual(400, response.status_code)

    def test_empty_firstname(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_firstname),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Firstname cannot be empty")
        self.assertEqual(400, response.status_code)

    def test_empty_lastname(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_lastname),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Lastname cannot be empty")
        self.assertEqual(400, response.status_code)

    def test_empty_othername(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_othername),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Othername cannot be empty")
        self.assertEqual(400, response.status_code)

    def test_empty_phonenumber(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_phonenumber),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "You must provide a phone number")
        self.assertEqual(400, response.status_code)

    def test_empty_passport_url(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_passport_url),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Passport url is needed")
        self.assertEqual(400, response.status_code)

    def test_empty_password(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_password),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Password is empty")
        self.assertEqual(400, response.status_code)

    def test_empty_password_confirm(self):
        response = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.empty_password_confirm),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Password confirm is empty")
        self.assertEqual(400, response.status_code)

    # login tests
    def test_login(self):
        resp = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.user_signs),
                                    content_type='application/json')
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.login),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Logged in as {}".format(self.login['email']))
        self.assertEqual(200, response.status_code)

    def test_login_abort(self):
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.login),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "current transaction is aborted")
        self.assertEqual(500, response.status_code)

    def test_login_invalid_email(self):
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.bad_email_format),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Email format is invalid")
        self.assertEqual(400, response.status_code)

    def test_login_invalid_credentials(self):
        resp = self.Client.post('/api/v2/auth/signup',
                                    data=json.dumps(self.user_signs),
                                    content_type='application/json')
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.invalid_credentials),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Invalid credentials")
        self.assertEqual(400, response.status_code)

    def test_login_empty_email(self):
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.login_empty_email),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "You must provide an email")
        self.assertEqual(400, response.status_code)

    def test_login_empty_password(self):
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.login_empty_password),
                                    content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "You must provide a password ")
        self.assertEqual(400, response.status_code)

    def tearDown(self):
        schema_user = """DROP TABLE if exists "users";"""
        schemas = [schema_user]
        for schema in schemas:
            if schema:
                self.cur.execute(schema)


if __name__ == '__main__':
    unittest.main()
