from flask import Flask
from flask_restful import Resource, Api
from collections import defaultdict

app = Flask(__name__)
api = Api(app)
items = defaultdict(int)


class Api(Resource):
    def get(self, name):
        return items['name']

    def post(self, name):
        items['name']+=1
        return "homepage +1"


class Apicount(Resource):
    def get(self,name):
        return {'homepage':items['name']}



api.add_resource(Api, '/api/pixel/<string:name>')
api.add_resource(Apicount, '/api/count/<string:name>')

app.run(port=5000, debug=True)

