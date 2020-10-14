import mysql.connector
from flask import Flask
from mysql.connector import Error
from mysql.connector import pooling



app = Flask(__name__)

def db_conn():
    try:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool",
                                                                      pool_size=1,
                                                                      autocommit=True,
                                                                      pool_reset_session=False,
                                                                      host='localhost',
                                                                      database='register',
                                                                      user='root',
                                                                      password='')
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    return connection_pool




@app.route('/api/pixel/<string:name>')
def increment_counter(name):

    connection_object = db_conn().get_connection()
    if connection_object.is_connected():
        print("Connection ID:", connection_object.connection_id)
        cursor = connection_object.cursor()
        cursor.execute("SELECT count FROM app where apiname = %s", (name,))
        myresult = cursor.fetchone()
        if myresult == None:
            cursor.execute("insert into app(`apiname`,`count`)values(%s,1)", (name,))
        else:
            cursor.execute("UPDATE app SET count = count + 1 WHERE apiname = %s", (name,))
        cursor.close()
        connection_object.close()
        print("MySQL connection is closed")

    return "okdb"


@app.route('/api/count/<string:name>')
def get_counter(name):

    connection_object = db_conn().get_connection()
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