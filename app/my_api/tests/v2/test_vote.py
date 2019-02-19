# test auth.py
import unittest
import os
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# local imports
from ...database import database, database_init
from app import create_app


class TestVote(unittest.TestCase):
    """docstring for TestVote."""
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
            "phonenumber": "0778082345",
            "passporturl": "jdkjfld.com",
            "password": "password",
            "passwordconfirm": "password"
        }
        # login variables
        self.login = {
            "email": "aloismburu@gmail.com",
            "password": "password"
        }

        self.apply_candidate = {
            "office": "National",
            "party": "Chap"
        }
        self.vote = {
            "president": "Jacob",
            "governor": "Noah",
            "mca": "Madiva"
        }

        with self.app.app_context():
            # init db creating tables
            database_init()

    # user signs up
    def test_user_candidature(self):
        resp = self.Client.post('/api/v2/auth/signup',
                                data=json.dumps(self.user_signs),
                                content_type='application/json')
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.login),
                                    content_type='application/json')
        respons1 = self.Client.post('/api/v2/vote/candidate',
                                    data=json.dumps(self.apply_candidate),
                                    content_type='application/json')
        result = json.loads(respons1.data.decode())
        self.assertEqual(result['Message'], "Your registration as a candidate is succesfull!")
        self.assertEqual(201, response.status_code)

    def test_vote(self):
        resp = self.Client.post('/api/v2/auth/signup',
                                data=json.dumps(self.user_signs),
                                content_type='application/json')
        response = self.Client.post('/api/v2/auth/login',
                                    data=json.dumps(self.login),
                                    content_type='application/json')
        respons1 = self.Client.post('/api/v2/vote/candidate',
                                    data=json.dumps(self.apply_candidate),
                                    content_type='application/json')
        respons2 = self.Client.post('/api/v2/vote',
                                    data=json.dumps(self.vote),
                                    content_type='application/json')
        result = json.loads(respons2.data.decode())
        self.assertEqual(result['Message'], "Vote casted!!!")
        self.assertEqual(201, response.status_code)

    def test_get_votes(self):
        response = self.Client.get('/api/v2/vote/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "These are the total votes gannered")
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        schema_user = """DROP TABLE if exists "users" CASCADE;"""
        schema_vote = """DROP TABLE if exists "vote" CASCADE;"""
        schemas = [schema_user, schema_vote]
        for schema in schemas:
            if schema:
                self.cur.execute(schema)


if __name__ == '__main__':
    unittest.main()
