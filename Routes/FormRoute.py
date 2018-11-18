from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
import Controllers.UserController as UserController
from bson.json_util import loads, dumps
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import Controllers.FormController as FormController

import storage as st

db = st.connect()

db_CN = st.connectCensusNight()

# Base de datos que simula la noche del censo
formAnswerCollection_CN = db_CN.formAnswerCollection_CN
AnswerMembersCollection_CN = db_CN.AnswerMembersCollection_CN

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


class censusNight(Resource):
    # @jwt_required
    def post(self):
        data = request.json
        start = data['start']
        if start:
            messages, success = FormController.censusNight(
                formAnswerCollection, AnswerMembersCollection, formAnswerCollection_CN, AnswerMembersCollection_CN)
        else:
            messages = 'No start Census Night'
            success = False

        return {
            "messages": messages,
            "success": success
        }


class getFormbyPeople(Resource):
    # @jwt_required
    def post(self):
        print("Llege a people")
        data = parserAnswerMembers.parse_args()
        Form = FormController.getFormByPeople(AnswerMembersCollection, data)
        return {
            "form": Form
        }


# Este solo debe ser llamado la primera vez luego utilizar update


class insertAnswersPeople(Resource):
    # @jwt_required
    def post(self):
        form = request.json
        CFN = form['CFN']
        ECN = form['ECN']
        idNumber = form['idNumber']
        messages, success = FormController.insertAnswersPeople(
            AnswerMembersCollection, ECN, CFN, idNumber, form)
        return {
            "messages": messages,
            "success": success
        }


class findSection(Resource):
    # @jwt_required
    def get(self):
        CFN = request.args['CFN']
        ECN = request.args['ECN']
        number = request.args['number']
        res = FormController.findSection(
            formAnswerCollection, ECN, CFN, number)
        if res:
            return res
        return None


class updateSection(Resource):
    # @jwt_required
    def put(self):
        data = request.json
        CFN = request.args['CFN']
        ECN = request.args['ECN']
        number = request.args['number']
        message, success = FormController.updateSection(
            formAnswerCollection, CFN, ECN, number, data)
        return {
            'message': message,
            'success': success
        }


class showStatistics(Resource):
    @jwt_required
    def get(self):
        data = FormController.getStatistics(
            formAnswerCollection, db.collector_codes)
        return data


class confirmForm(Resource):
    # @jwt_required
    def post(self):
        data = request.json
        ECN = data['ECN']
        CFN = data['CFN']
        message, success = FormController.confirmForm(
            formAnswerCollection, ECN, CFN)
        return {
            'message': message,
            'success': success
        }


class familyIdentifiers(Resource):
    # @jwt_required
    def post(self):
        data = request.json
        ECN = data['ECN']
        CFN = data['CFN']
        return {
            "family_identifiers": FormController.familyIdentifiers(ECN, CFN, AnswerMembersCollection)
        }
