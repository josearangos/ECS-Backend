from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import Controllers.CollectorController as CollectorController

import storage as st
db = st.connect()
# collection donde estan toda la info de los analistas
CollectorCollection = db.collectors
CollectorCodesCollection = db.collectors_codes

# para validar que el JSON del body tenga los campos
parser = reqparse.RequestParser()
parser.add_argument('id', help='This field cannot be blank', required=True)
parser.add_argument(
    'password', help='This field cannot be blank', required=True)

# validar todo los campos al momento de registrar un collector
parserCollector = reqparse.RequestParser()
parserCollector.add_argument(
    'id', help='This field cannot be blank', required=True)
parserCollector.add_argument(
    'fullName', help='This field cannot be blank', required=True)
parserCollector.add_argument(
    'password', help='This field cannot be blank', required=True)
parserCollector.add_argument(
    'cellphone', help='This field cannot be blank', required=True)


class collectorLogin(Resource):
    def post(self):
        data = parser.parse_args()
        access_token, refresh_token = CollectorController.login(
            CollectorCollection, data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


class collectorTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class registreCollector(Resource):
    # @jwt_required  # esta notacion indica que necesita obligatoriamente un token
    def post(self):
        data = request.json
        id = data['id']
        success, message = CollectorController.registre(
            CollectorCollection, id, data)
        return {'message': message, "success": success}


class findCollector(Resource):
    # @jwt_required
    def get(self):
        id = request.args
        data, status = CollectorController.find(
            CollectorCollection, id['id'])
        return data, status
class showCodes(Resource):
    # @jwt_required
    def get(self):
        collectorId = request.args
        data, status = CollectorController.getCodes(CollectorCodesCollection, collectorId['id'])
        return data, status
