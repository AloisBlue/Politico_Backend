# test for offices

import unittest
import json

from app import create_app

class TestOffices(unittest.TestCase):
    """docstring for TestOffices."""
    def setUp(self):
        self.app = create_app('testing')
        self.Client = self.app.test_client()
        self.offices_list = [

        ]
        self._id = len(self.offices_list) + 1
        self.make_office = {
            'id': self._id,
            'name': 'President',
            'type': 'National'
        }

    def test_create_office(self):
        response = self.Client.post('/api/v1/offices', data=json.dumps(self.make_office), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Office registered in the system!!!")
        self.assertEqual(201, response.status_code)

    def test_office_exists(self):
        response = self.Client.post('/api/v1/offices', data=json.dumps(self.make_office), content_type='application/json')
        response1 = self.Client.post('/api/v1/offices', data=json.dumps(self.make_office), content_type='application/json')
        result = json.loads(response1.data.decode())
        self.assertEqual(result['Message'], "The office is already registered in our system")
        self.assertEqual(400, response1.status_code)

    def test_get_all_offices(self):
        response = self.Client.get('/api/v1/offices', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "The following include office registered in the system")
        self.assertEqual(200, response.status_code)

    def test_get_particular_office(self):
        response = self.Client.get('/api/v1/offices/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Office was found!!!")
        self.assertEqual(200, response.status_code)

    def test_get_particular_office_when_none(self):
        response = self.Client.get('/api/v1/offices/14', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Either there is no such office or your Id is invalid")
        self.assertEqual(404, response.status_code)

if __name__ == "__main__":
    unittest.main()
