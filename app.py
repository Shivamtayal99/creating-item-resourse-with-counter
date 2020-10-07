from flask import Flask,request
from flask_restful import Resource, Api
from collections import defaultdict
import mysql.connector

app = Flask(__name__)
api = Api(app)
items = defaultdict(int)


@app.route('/api/pixel/<string:name>',methods=['POST','GET'])
def increment_counter(name):
    items[name] += 1

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="register"
    )
    mycursor = mydb.cursor()
    if request.method == 'GET':

        mycursor.execute("insert into api(`apiname`,`count`)values(%s,1) on duplicate key update `count` = `count`+1",(name,))

        mydb.commit()
        mycursor.close()
        return "Ok"



@app.route('/api/count/<string:name>')
def get_counter(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="register"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT count FROM api where apiname = %s",(name,))

    myresult = mycursor.fetchone()
    return str(myresult[0])


app.run(port=5000, debug=True)

