# app/my_api/v1/party.py
from flask_restful import Resource, reqparse
import validators

# Storage
parties_list = [

]


class CreateParty(Resource):
    """docstring for CreateParty."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name of the party should be filled"
    )
    parser.add_argument(
        'hqAddress',
        type=str,
        required=True,
        help="Head quarter address needed"
    )
    parser.add_argument(
        'logUrl',
        type=str,
        required=True,
        help="Logo url needed"
    )

    @classmethod
    def post(self):
        data = CreateParty.parser.parse_args()
        party_exist = [party for party in parties_list if party['name'] == data['name']]
        if (len(party_exist) != 0):
            return {'Message': 'The party is already registered'}, 400
        _id = len(parties_list) + 1
        new_party = {
            'id': _id,
            'name': data['name'],
            'hqAddress': data['hqAddress'],
            'logUrl': data['logUrl']
            }
        # validation
        if not data['name'] or not data['hqAddress'] or not data['logUrl']:
            return {'Message': 'Check for empty fields'}
        elif len(data['name']) < 3 or len(data['name']) > 15:
            return {'Message': 'Name must be between 3 and 15 characters'}
        elif len(data['hqAddress']) < 3 or len(data['hqAddress']) > 20:
            return {'Message': 'Head quarter address must be between 3 and 20 characters'}
        elif not validators.url(data['logUrl']):
            return {'Message': 'You must provide a valid url'}
        else:
            parties_list.append(new_party)
            return {'Message': 'Party registered!!!', 'Party': new_party}, 201


class GetAllParties(Resource):
    """docstring for getting all parties."""
    @classmethod
    def get(self):
        if not parties_list:
            return {'Message': 'There is no party in our database'}, 404
        else:
            return {'Message': 'The following include our parties', 'All Parties': parties_list}, 200


class PartyById(Resource):
    """docstring for PartyById."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str
    )
    parser.add_argument(
        'hqAddress',
        type=str
    )
    parser.add_argument(
        'logUrl',
        type=str
    )

    @classmethod
    def get(self, party_id):
        get_party = [party for party in parties_list if party['id'] == party_id]
        if len(get_party) == 0:
            return {'Message': "Either there is no such party or id is invalid"}, 404
        return {'Message': 'Party found!!!', 'Party': get_party[0]}, 200

    @classmethod
    def put(self, party_id):
        data = PartyById.parser.parse_args()
        get_party = [party for party in parties_list if party['id'] == party_id]
        check_exists = [party for party in parties_list if party['name'] == data['name']]
        if len(get_party) == 0:
            return {'Message': 'Invalid id, confirm the id of your party'}, 404
        elif len(check_exists) != 0:
            return {'Message': 'That party already exists'}, 400
        else:
            get_party[0].update(data)
            return {'Message': 'Your party update is successful',
                    'Party': get_party[0]}, 200

    @classmethod
    def delete(self, party_id):
        check_exists = [party for party in parties_list if party['id'] == party_id]
        if len(check_exists) == 0:
            return {'Message': 'Invalid id, confirm the id of the party'}, 404
        else:
            parties_list.remove(check_exists[0])
            return {'Message': 'The party was successfully removed from the system'}, 200
