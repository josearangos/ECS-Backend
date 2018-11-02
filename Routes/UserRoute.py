from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
import Controllers.UserController as UserController
from bson.json_util import loads, dumps
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)


# se importan los modelos con los cuales serviran para que la app sea mas mantenible
# Este repositorio es interesantes
# https://github.com/tomasrasymas/flask-restful-api-template

import storage as st
db = st.connect()

codeCollection = db.codes  # collection donde estan los codigos del censo


# para validar que el JSON del body tenga los campos
parser = reqparse.RequestParser()
parser.add_argument('ECS', help='This field cannot be blank', required=True)
parser.add_argument('CNF', help='This field cannot be blank', required=True)


class insertCode(Resource):
    def post(self):
        data = parser.parse_args()  # capturo el valor por la URL
        return {'you user is': data}, 201


class userLogin(Resource):
    def post(self):
        data = parser.parse_args()
        access_token, refresh_token = UserController.login(
            codeCollection, data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


class SecretResource(Resource):
    @jwt_required  # esta notacion indica que necesita obligatoriamente un token
    def get(self):
        return {
            'answer': 42
        }


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


"""
Para saber el usuario actual con el token se usa
current_user = get_jwt_identity()
print("usuario activo", current_user)
"""
