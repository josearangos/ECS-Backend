from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

import utils.json_encoder as encoder


def getFormByPeople(AnswerMembersCollection, data):
    Form = "null"
    try:
        Form = AnswerMembersCollection.find_one({
            'ECN': data.ECN,
            'CFN': data.CFN,
            'idNumber': data.idNumber
        }, {'_id': False})
    except Exception as e:
        print(e)
    return Form

# Validar que traiga todo los campos de las preguntas


def insertAnswersPeople(AnswerMembersCollection, data) -> tuple:
    messages = ""
    success = False
    try:
        responde = AnswerMembersCollection.find_one_and_update(
            {'idNumber': data.idNumber},
            {'$set': {"ECN": data.ECN, "CFN": data.CFN,
                      "idNumber": data.idNumber, "questions": [data.questions]}}, upsert=True)
    except Exception as e:
        print(e)
        messages = str(e)
    else:
        success = True
        messages = 'responses of the person recorded successfully'
    return messages, success
