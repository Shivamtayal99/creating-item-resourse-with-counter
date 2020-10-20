import mysql.connector
from flask import Flask
from kafka import KafkaProducer
import json
from mysql.connector import pooling


app = Flask(__name__)
def json_serializer(data):
    return json.dumps(data).encode('utf-8')
producer=KafkaProducer(bootstrap_servers=['192.168.56.1:9092'],value_serializer=json_serializer)




connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool",
                                                              pool_size=12,
                                                              autocommit=True,
                                                              pool_reset_session=False,
                                                              host='localhost',
                                                              database='register',
                                                              user='root',
                                                              password='')





@app.route('/api/pixelKafka/<string:name>')
def push_data(name):
    register_api = {"page": name, "count": 1}
    print(register_api)
    producer.send("register_api", register_api)
    return "ok kafka"
@app.route('/api/pixel/<string:name>')
def increment_counter(name):

    connection_object = connection_pool.get_connection()
    if connection_object.is_connected():
        print("Connection ID:", connection_object.connection_id)
        cursor = connection_object.cursor()
        cursor.execute("insert into app(`apiname`,`count`)values(%s,1) on duplicate key update `count` = `count`+1",
                         (name,))
        cursor.close()
        connection_object.close()
        print("MySQL connection is closed")

    return "okdb"


@app.route('/api/count/<string:name>')
def get_counter(name):

    connection_object = connection_pool.get_connection()
    if connection_object.is_connected():
        cursor = connection_object.cursor()
        cursor.execute("SELECT count FROM app where apiname = %s", (name,))
        myresult = cursor.fetchone()
        cursor.close()
        connection_object.close()

        if myresult == None:
            return str(0)

        return str(myresult[0])


app.run(port=5000, debug=True)