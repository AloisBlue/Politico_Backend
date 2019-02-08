# app/api/v1/party.py
from flask_restful import Resource, reqparse

# Dictionary
Parties = [

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
        party_exist = [party for party in Parties if party['name'] == data['name']]
        if (len(party_exist) != 0):
            return {'Message': 'The party is already registered'}, 400
        _id = len(Parties) + 1
        new_party = {
            'id': _id,
            'name': data['name'],
            'hqAddress': data['hqAddress'],
            'logUrl': data['logUrl']
            }
        Parties.append(new_party)
        return {'message': 'Party registered!!!', 'Party': new_party}, 201
