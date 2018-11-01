from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)


def login(codeCollection, data) -> tuple:
    access_token = "null"
    refresh_token = "null"
    try:
        ECS = data.ECS
        CNF = data.CNF
        codes_response = codeCollection.find_one({"ECS": ECS})
    except Exception as e:
        print(e)
    else:
        if codes_response is not None:
            if codes_response['CNF'] == CNF:
                # el token solo tiene una duracion de 15 minutos
                access_token = create_access_token(identity=data.ECS)
                # con este se puede renovar el acces_token
                refresh_token = create_refresh_token(identity=data.ECS)
    return access_token, refresh_token


