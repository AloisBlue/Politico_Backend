# app/my_api/v1/offices.py

from flask_restful import Resource, reqparse

offices_list = [

]

class CreateOffice(Resource):
    """docstring for CreateOffice."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name of the political office missing"
    )
    parser.add_argument(
        'type',
        type=str,
        required=True,
        help="Type of the office not stated"
    )

    @classmethod
    def post(self):
        data = CreateOffice.parser.parse_args()
        office_exist = [office for office in offices_list if office['name'] == data['name']]
        if (len(office_exist) != 0):
            return {'Message': 'The office is already registered in our system'}, 400
        _id = len(offices_list) + 1
        new_office = {
            'id': _id,
            'name': data['name'],
            'type': data['type']
            }
        offices_list.append(new_office)
        return {'Message': 'Office registered in the system!!!', 'Office': new_office}, 201

class GetAllOffices(Resource):
    """docstring for GetAllOffices."""
    @classmethod
    def get(self):
        if not offices_list:
            return {'Message': 'No office registered in the system yet'}, 404
        else:
            return {'Message': 'The following include office registered in the system',
                        'Office': offices_list}, 200

class OfficeById(Resource):
    """docstring for OfficeById."""
    @classmethod
    def get(self, office_id):
        exists_office = [office for office in offices_list if office['id'] == office_id]
        if len(exists_office) == 0:
            return {'Message': 'Either there is no such office or your Id is invalid'}, 404
        else:
            return {'Message': 'Office was found!!!',
                        'Office': exists_office[0]}, 200
