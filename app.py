
from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/api/pixel/<string:name>')
def increment_counter(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="register"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count FROM app where apiname = %s", (name,))
    myresult = mycursor.fetchall()
    if myresult == None:
        mycursor.execute("insert into app(`apiname`,`count`)values(%s,1)",(name,))
    else:
        mycursor.execute("UPDATE app SET count = count + 1 WHERE apiname = %s",(name,))
    mydb.commit()
    mycursor.close()
    return "Ok db"


@app.route('/api/count/<string:name>')
def get_counter(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="register"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count FROM app where apiname = %s", (name,))
    myresult = mycursor.fetchone()
    mydb.commit()
    mycursor.close()
    if myresult == None:
        return str(0)
    return str(myresult[0])


app.run(port=5000, debug=True)

