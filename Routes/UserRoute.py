from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal

# se importan los modelos con los cuales serviran para que la app sea mas mantenible
# Este repositorio es interesantes
# https://github.com/tomasrasymas/flask-restful-api-template


class user(Resource):
    def get(self):
        return {'hello': 'world! user'}

    def post(self):
        data = request.get_json()  # capturo el valor por la URL
        return {'you user is': data}, 201
