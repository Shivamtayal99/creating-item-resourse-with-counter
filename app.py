
from flask import Flask
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

app = Flask(__name__)


@app.route('/api/pixel/<string:name>')
def increment_counter(name):
    try:
        connection_pool  = mysql.connector.pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                                       pool_size=1,
                                                                       pool_reset_session=False,
                                                                       host='localhost',
                                                                       database='register',
                                                                       user='root',
                                                                       password='')
        connection_object = connection_pool.get_connection()
        if connection_object.is_connected():
            print("Connection ID:", connection_object.connection_id)
            cursor = connection_object.cursor()
            cursor.execute("insert into app(`apiname`,`count`)values(%s,1) on duplicate key update `count` = `count`+1",
                           (name,))
            cursor.close()
            connection_object.close()
            print("MySQL connection is closed")






    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)







    return "okdb"


@app.route('/api/count/<string:name>')
def get_counter(name):
    try:
        connection_pool  = mysql.connector.pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                                       pool_size=1,
                                                                       pool_reset_session=True,
                                                                       host='localhost',
                                                                       database='register',
                                                                       user='root',
                                                                       password='')
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




    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)

app.run(port=5000, debug=True)

