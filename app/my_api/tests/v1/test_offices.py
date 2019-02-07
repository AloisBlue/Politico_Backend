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

if __name__ == "__main__":
    unittest.main()
