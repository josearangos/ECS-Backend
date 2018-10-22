from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import config
from json import dumps
import unittest


app = Flask(__name__)

# Importamos la configuracion global de nuestra app
app.config.from_pyfile('config.py')

mongo = PyMongo(app)

# manejo e errores en las peticiones


@app.route('/categorys', methods=['GET'])
def get_all_categorys():
    Mycategorys = mongo.db.categorys
    output = []

    for q in Mycategorys.find():
        output.append(
            {'nombre': q['nombre'], 'descripcion': q['descripcion']})
        print(q)

    return jsonify({'categorys': output})


@app.route('/categorys', methods=['POST'])
def insert_category():
    Mycategorys = mongo.db.categorys
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']

    Mycategorys.insert({'nombre': nombre, 'descripcion': descripcion})

    return jsonify({'message': 'done'})


@app.route('/categorys', methods=['PUT'])
def update_category():
    Mycategorys = mongo.db.categorys
    id = request.json['id']
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']

    output = Mycategorys.update_one(
        {'_id': id},
        {'$set': {'nombre': nombre, 'descripcion': descripcion}},
        upsert=True)

    return jsonify({'message': 'done'})


@app.route('/categorys', methods=['DELETE'])
def delete_category():
    id = request.json['id']
    Mycategorys = mongo.db.categorys
    Mycategorys.delete_one({'_id': id})
    return jsonify({'message': 'done'})


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


class TestCategory(unittest.TestCase):

    #Si se pasa un id menor o igual a cero mediante el setter respectivo, deberá generarse una IllegalArgumentException.#

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


# if __name__ == '__main__':  unittest.main()

if __name__ == '__main__':
    app.run()
