from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import config
import pymongo


app = Flask(__name__)


# Adding JWT
app.config['JWT_SECRET_KEY'] = 'pepitoperezcarvajales'
jwt = JWTManager(app)
# Importamos la configuracion global de nuestra app
app.config.from_pyfile('config.py')
# asigamos el prefijo "ECS/Api/v1" a todas las rutas
api = Api(app, config.urlPrefix)


# manejo de errores en las peticiones
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


# importamos todas las rutas de nuestra API
# Usuario
from Routes.UserRoute import userLogin, insertCode, SecretResource, TokenRefresh
# Analista
from Routes.AnalistRoute import analistLogin, analistTokenRefresh, findAnalist
# Collector
from Routes.CollectorRoute import collectorLogin, collectorTokenRefresh, registreCollector, findCollector

# Todo lo que tiene que ver con el formulario
from Routes.FormRoute import getFormbyPeople, insertAnswersPeople


# Usuario
api.add_resource(userLogin, '/user/login', '/user/login')
api.add_resource(insertCode, '/code/insert', '/code/insert')
api.add_resource(SecretResource, '/secret', '/secret')
api.add_resource(TokenRefresh, '/user/tokenRefresh', '/user/tokenRefresh')

# Analista
api.add_resource(analistLogin, '/analist/login', '/analist/login')
api.add_resource(analistTokenRefresh, '/analist/tokenRefresh',
                 '/analist/tokenRefresh')
api.add_resource(findAnalist, '/analist/show_analist', '/analist/show_analist')
# Collector
api.add_resource(registreCollector, '/collector/registre',
                 '/collector/registre')
api.add_resource(findCollector, '/collector/show_collector',
                 '/collector/show_collector')
api.add_resource(collectorLogin, '/collector/login', '/collector/login')
api.add_resource(collectorTokenRefresh,
                 '/collector/tokenRefresh', '/analist/tokenRefresh')

# Formulario

api.add_resource(getFormbyPeople, '/user/get_form/member',
                 '/user/get_form/member')

api.add_resource(insertAnswersPeople, '/user/insert_answers/member',
                 '/user/insert_answers/member')


if __name__ == '__main__':
    app.run()
