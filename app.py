from flask import Flask
from flask_restful import Resource, Api
from collections import defaultdict

app = Flask(__name__)
api = Api(app)
items = defaultdict(int)





@app.route('/api/pixel/<string:name>')
def increment_counter(name):
    items[name] += 1
    return "Ok"
@app.route('/api/count/<string:name>')
def get_counter(name):
    return str(items[name])





app.run(port=5000, debug=True)

