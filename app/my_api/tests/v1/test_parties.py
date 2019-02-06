import unittest
import json

from app import create_app


class TestParties(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.Client = self.app.test_client()
        self.parties_list = [

        ]
        self._id = len(self.parties_list) + 1
        self.new_party = {
            'id': self._id,
            'name': 'Chap',
            'hqAddress': 'Nairobi',
            'logUrl': 'http://logo.com'
            }

    def test_create_party(self):
        """
        Give a status 201 of when a  is created
        """
        response = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
