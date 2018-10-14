from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import config

app = Flask(__name__)

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
from Routes.UserRoute import user

api.add_resource(user, '/user', '/user')

if __name__ == '__main__':
    app.run()
