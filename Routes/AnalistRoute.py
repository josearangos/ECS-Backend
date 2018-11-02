from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import Controllers.AnalistController as AnalistController

import storage as st
db = st.connect()
# collection donde estan toda la info de los analistas
AnalistCollection = db.analists


# para validar que el JSON del body tenga los campos
parser = reqparse.RequestParser()
parser.add_argument('id', help='This field cannot be blank', required=True)
parser.add_argument(
    'password', help='This field cannot be blank', required=True)


class analistLogin(Resource):
    def post(self):
        data = parser.parse_args()
        access_token, refresh_token = AnalistController.login(
            AnalistCollection, data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


class analistTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
class findAnalist(Resource):
    #@jwt_required
    def get(self):
        id = request.args
        data, status = collector = AnalistController.find(AnalistCollection, id['id'])
        return data, status