from flask import Flask
from flask_restful import Resource,Api



app=Flask(__name__)
api=Api(app)
items=[]
class Item(Resource):
    def get(self,name):
        for item in items:
            if item['name']==name:
                return item
        return {'item':None}

    def post(self,name):
        for item in items:
            if item['name'] == name:
                item['count']+=1
                return item


        count = 0
        value = count + 1
        item={'name':name,'count':value}
        items.append(item)
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items}
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')





app.run(port=5000,debug=True)
