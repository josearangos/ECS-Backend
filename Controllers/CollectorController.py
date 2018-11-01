from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)


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


def registre(CollectorCollection, data) -> tuple:
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
