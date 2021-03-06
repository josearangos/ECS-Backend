from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

from flask import json, jsonify
from pymongo import ReturnDocument

import Models.CollectorModel as model
import utils.json_encoder as encoder


def login(codeCollection, data) -> tuple:
    access_token = "null"
    refresh_token = "null"
    try:
        id = data.id
        password = data.password
        codes_response = codeCollection.find_one({"id": id})
    except Exception as e:
        print(e)
    else:
        if codes_response is not None:
            if codes_response['password'] == password:
                # el token solo tiene una duracion de 15 minutos
                access_token = create_access_token(identity=data.id)
                # con este se puede renovar el acces_token
                refresh_token = create_refresh_token(identity=data.id)
    return access_token, refresh_token


def registre(CollectorCollection, id, data) -> tuple:
    message = ""
    success = False
    try:
        CollectorCollection.insert(data)
    except Exception as e:
        print(e)
        message = str(e)
    else:
        success = True
        message = 'User save successfully'
    return success, message


def find(CollectorCollection, id) -> tuple:
    collector = model.Collector()
    _retcollector = collector.get(id)
    print(_retcollector)
    if _retcollector:
        return _retcollector, 200
    return None, 404


def getCodes(CollectorCodeCollection, collectorId) -> tuple:
    # print(id)
    data = CollectorCodeCollection.find(
        {'collectorId': collectorId}, {'_id': False, 'collectorId': False})
    res = []
    for doc in data:
        res.append(doc)
    if data:
        return res, 202
    else:
        return None, 404


def deliverCode(CollectorCodesCollection, ECN, CFN, collectorId):
    res = CollectorCodesCollection.find_one_and_update({
        'ECN': ECN,
        'CFN': CFN,
        'collectorId': collectorId
    }, {
        '$set': {
            'entregado': True
        }
    }, return_document=ReturnDocument.AFTER,
        projection={
            '_id': False
        },
        upsert=False)
    success = False
    message = ""
    if res:
        success = True
        message = "the code was delivered successfully"
    else:
        success = False
        message = "the code was not delivered successfully"
    return message, success
