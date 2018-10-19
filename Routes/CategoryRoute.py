from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from pymongo import MongoClient
import config

mongo_client = MongoClient(config.MONGO_URI)

categorydb = mongo_client.adminCategory


class category(Resource):
    def get(self):
        return {'get': categorydb.find({})}

    def post(self):
        data = request.get_json()  # capturo el valor por la URL
        print(data)
        return {'post': data}, 201

    def put(self):
        data = request.get_json()  # capturo el valor por la URL
        return {'put': data}, 201

    def delete(self):
        data = request.get_json()  # capturo el valor por la URL
        return {'delete': data}, 201
