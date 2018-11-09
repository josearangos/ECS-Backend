from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
import Controllers.UserController as UserController
from bson.json_util import loads, dumps
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import Controllers.FormController as FormController

import storage as st
db = st.connect()

formBaseCollection = db.form  # collection donde estan los codigos del censo


# para validar que el JSON del body tenga los campos
parser = reqparse.RequestParser()
parser.add_argument('ECS', help='This field cannot be blank', required=True)
parser.add_argument('CNF', help='This field cannot be blank', required=True)


class SecretResource(Resource):
    # @jwt_required  # esta notacion indica que necesita obligatoriamente un token
    def get(self):
        data = parser.parse_args()
        Form = FormController.getFormBase(formBaseCollection, data)
        return {
            "form": Form
        }
