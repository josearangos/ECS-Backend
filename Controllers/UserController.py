from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)


def login(codeCollection, data) -> tuple:
    access_token = "null"
    refresh_token = "null"
    try:
        ECN = data.ECN
        CFN = data.CFN
        codes_response = codeCollection.find_one({"ECN": ECN})
    except Exception as e:
        print(e)
    else:
        if codes_response is not None:
            if codes_response['CFN'] == CFN:
                # el token solo tiene una duracion de 15 minutos
                access_token = create_access_token(
                    identity=data.ECN+'*'+data.CFN)
                # con este se puede renovar el acces_token
                refresh_token = create_refresh_token(
                    identity=data.ECN+'*'+data.CFN)
    return access_token, refresh_token


def currentEntity(access_token):
    current_entity = get_jwt_identity()
    print(current_entity)
    isUser = current_entity.find('*')
    if isUser != -1:
        ECN = current_entity[0:isUser]
        CFN = current_entity[isUser+1:len(current_entity)]
        return{
            "isUser": True,
            "ECN": ECN,
            "CFN": CFN
        }
    else:
        return{
            "isUser": False,
            "id": current_entity
        }
