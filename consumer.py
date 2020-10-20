
import mysql.connector
from kafka import KafkaConsumer
import json
from mysql.connector import pooling




connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool",
                                                              pool_size=12,
                                                              autocommit=True,
                                                              pool_reset_session=False,
                                                              host='localhost',
                                                              database='register',
                                                              user='root',
                                                              password='')



consumer = KafkaConsumer(
    "register_api",
    bootstrap_servers=['192.168.56.1:9092'],
    auto_offset_reset='earliest',
    group_id="consumer-group-a")


connection_object = connection_pool.get_connection()
if connection_object.is_connected():

    print("consumer start")
    print(consumer)
    for msg in consumer:
        print(type(msg))
        if msg is not None:
            p = json.loads(msg.value.decode('utf-8'))
            page=p['page']
            print('update count for',page)
            cursor = connection_object.cursor()
            cursor.execute("insert into app(`apiname`,`count`)values(%s,1) on duplicate key update `count` = `count`+1",
                           (page,))
        else:
            cursor.close()
            connection_object.close()









