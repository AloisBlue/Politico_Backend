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
        self.no_name = {
            'id': 2,
            'hqAddress': 'Mombasa',
            'logUrl': "klfjd.com"
        }
        self.no_add = {
            'id': 2,
            'name': 'casse',
            'logUrl': "klfjd.com"
        }
        self.no_url = {
            'id': 2,
            'name': 'casse',
            'hqAddress': "Voi"
        }
        self.edit_party = {
            'name': 'Mwamba',
            'hqAddress': 'Milangine',
            'logUrl': 'fdlf.com'
        }

    def test_create_party(self):
        """
        Give a status 201 of when a  is created
        """
        response = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Party registered!!!")
        self.assertEqual(201, response.status_code)

    def test_create_party_when_exists(self):
        """
        Give a status 400 of when party exists
        """
        response = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        response1 = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        result = json.loads(response1.data.decode())
        self.assertEqual(result['Message'], "The party is already registered")
        self.assertEqual(400, response1.status_code)

    def test_create_party_name_empty(self):
        """
        Return name to be filled as required data
        """
        response = self.Client.post('/api/v1/parties', data=json.dumps(self.no_name), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], {'name': 'Name of the party should be filled'})

    def test_create_party_address_empty(self):
        """
        Return address required
        """
        response = self.Client.post('/api/v1/parties', data=json.dumps(self.no_add), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], {'hqAddress': 'Head quarter address needed'})

    def test_create_party_url_empty(self):
        """
        Return url required to create party
        """
        response = self.Client.post('/api/v1/parties', data=json.dumps(self.no_url), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], {'logUrl': 'Logo url needed'})

    def test_get_particular_party(self):
        """
        Give a status of 200 when a particular party exists
        """
        response1 = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        response = self.Client.get('/api/v1/parties/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Party found!!!")
        self.assertEqual(200, response.status_code)

    def test_get_particular_party_when_none(self):
        """
        Give a status of 404 not found when a party by id doesn't exists
        """
        response = self.Client.get('/api/v1/parties/12', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Either there is no such party or id is invalid")
        self.assertEqual(404, response.status_code)

    def test_get_all_parties(self):
        """
        Status of 200
        """
        response1 = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        response = self.Client.get('/api/v1/parties', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "The following include our parties")
        self.assertEqual(200, response.status_code)

    def test_edit_party(self):
        """
        Give status 200 and test message on edit
        """
        response1 = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        response = self.Client.put('/api/v1/parties/1', data=json.dumps(self.edit_party), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Your party update is successful")
        self.assertEqual(200, response.status_code)

    def test_edit_with_same_data(self):
        """
        Give a status of 400 if party exists
        """
        response2 = self.Client.post('/api/v1/parties', data=json.dumps(self.new_party), content_type='application/json')
        response = self.Client.put('/api/v1/parties/1', data=json.dumps(self.edit_party), content_type='application/json')
        response1 = self.Client.put('/api/v1/parties/1', data=json.dumps(self.edit_party), content_type='application/json')
        result = json.loads(response1.data.decode())
        self.assertEqual(result['Message'], "That party already exists")
        self.assertEqual(400, response1.status_code)

    def test_delete_party(self):
        response = self.Client.delete('/api/v1/parties/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "The party was successfully removed from the system")
        self.assertEqual(200, response.status_code)

    def test_delete_party_when_none(self):
        response = self.Client.delete('/api/v1/parties/12', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['Message'], "Invalid id, confirm the id of the party")
        self.assertEqual(404, response.status_code)

if __name__ == '__main__':
    unittest.main()
