from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
import Controllers.UserController as UserController
from bson.json_util import loads, dumps
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import Controllers.FormController as FormController

import storage as st
db = st.connect()

# collection donde estan las respuestas del censo de todos los hogares
formAnswerCollection = db.formAnswer
# Collection donde estan las respuesta de cada integrante de un hogar
AnswerMembersCollection = db.AnswerMembers

# para validar que el JSON del body que trae el formulario por seciones tenga todos los campos
parserformAnswer = reqparse.RequestParser()
parserformAnswer.add_argument(
    'ECS', help='This field cannot be blank', required=True)
parserformAnswer.add_argument(
    'CNF', help='This field cannot be blank', required=True)

parserformAnswer.add_argument(
    'SECTION', help='This field cannot be blank', required=True)

# para validar que el JSON del body que trae el formulario de cada integrante del hogar tenga todos los campos
parserAnswerMembers = reqparse.RequestParser()
parserAnswerMembers.add_argument(
    'ECN', help='This field cannot be blank', required=True)
parserAnswerMembers.add_argument(
    'CFN', help='This field cannot be blank', required=True)

parserAnswerMembers.add_argument(
    'idNumber', help='This field cannot be blank', required=True)

# Para validar que las peticiones de insertar respuesta y actualizar respuesta por persona, traigan todo los datos
parserAnswerMembersIU = reqparse.RequestParser()
parserAnswerMembersIU.add_argument(
    'ECN', help='This field cannot be blank', required=True)
parserAnswerMembersIU.add_argument(
    'CFN', help='This field cannot be blank', required=True)

parserAnswerMembersIU.add_argument(
    'idNumber', help='This field cannot be blank', required=True)

parserAnswerMembersIU.add_argument(
    'questions', help='This field cannot be blank', required=True)


class getFormbyPeople(Resource):
    # @jwt_required
    def post(self):
        data = parserAnswerMembers.parse_args()
        Form = FormController.getFormByPeople(AnswerMembersCollection, data)
        return {
            "form": Form
        }

# Este solo debe ser llamado la primera vez luego utilizar update


class insertAnswersPeople(Resource):
    # @jwt_required
    def post(self):
        data = parserAnswerMembersIU.parse_args()
        messages, success = FormController.insertAnswersPeople(
            AnswerMembersCollection, data)
        return{
            "messages": messages,
            "success": success
        }
