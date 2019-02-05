# app/api/v1/party.py
from flask_restful import Resource, reqparse

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
        parties_list.append(new_party)
        return {'Message': 'Party registered!!!', 'Party': new_party}, 201

class GetAllParties(Resource):
    """docstring for getting all parties."""
    def get(self):
        if not parties_list:
            return {'Message': 'There is no party in our database'}, 404
        else:
            return {'Message': 'The following include our parties', 'All Parties': parties_list}, 200
