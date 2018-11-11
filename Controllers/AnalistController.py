from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
import Models.AnalistModel as model
import utils.json_encoder as encoder


def login(AnalistCollection, data) -> tuple:
    access_token = "null"
    refresh_token = "null"
    try:
        id = data.id
        password = data.password
        codes_response = AnalistCollection.find_one({"id": id})
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


def find(AnalistCollection, id) -> tuple:
    analist = model.Analist()
    _retanalist = analist.get(id)
    if _retanalist:
        return _retanalist, 202
    return None, 404
def insert(AnalistCollection, id, fullName, password, state):
    analist = model.Analist()
    res = analist.insert(id, fullName, password, state)
    message = ""
    success = False
    if res:
        message =  "Analista ingresado con exito"
        success = True
    else:
        message =  "Hubo error al ingresar el analista"
        success = False
    return message, success
