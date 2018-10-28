from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
import storage as st
from bson.json_util import loads, dumps
# se importan los modelos con los cuales serviran para que la app sea mas mantenible
# Este repositorio es interesantes
# https://github.com/tomasrasymas/flask-restful-api-template

db = st.connect()

class user(Resource):
    def get(self):
        record = db.cl_users_v1.find_one()
        json_str = dumps(record)
        return {'hello': json_str}
    def post(self):
        data = request.get_json()  # capturo el valor por la URL
        print(data)
        return {'you user is': data}, 201