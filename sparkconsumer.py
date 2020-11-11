from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import mysql.connector
from mysql.connector import pooling


def upsertToDelta(row,epoch_id):
    rows=row.select('page','count').collect()
    print(rows)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="register"
    )

    cursor = mydb.cursor()
    for i in rows:
        print(i[0])
        print(i[1])
        page1=i[0]
        count1=int(i[1])
        print("consumer start")
        cursor.execute("CREATE TABLE IF NOT EXISTS customers (page VARCHAR(10) PRIMARY KEY, count INT)")
        cursor.execute("insert into customers(`page`,`count`)values(%s,%s) on duplicate key update `count` = `count`+%s",
                       (page1,count1,count1))
        mydb.commit()
        cursor.close()






# Set Kafka config
kafka_broker_hostname='192.168.56.1'
kafka_consumer_portno='9092'
kafka_broker=kafka_broker_hostname + ':' + kafka_consumer_portno
kafka_topic_input='register_api'


spark = SparkSession.builder.appName("Api").getOrCreate()



spark.sparkContext.setLogLevel("WARN")
df_kafka = spark.readStream \
                .format("kafka") \
                        .option("kafka.bootstrap.servers", kafka_broker) \
                                .option("subscribe", kafka_topic_input) \
                                        .load()
df_kafka.printSchema()
# Convert data from Kafka broker into String type
df_kafka_string = df_kafka.selectExpr("CAST(value AS STRING) as value")

df_schema = StructType() \
                .add("page", StringType()) \
                        .add("count", IntegerType())

df_kafka_string_parsed=df_kafka_string.select(from_json(df_kafka_string.value,df_schema).alias("df_data"))

df_kafka_string_formatted=df_kafka_string_parsed.select(
        col("df_data.page").alias("page"),
        col("df_data.count").alias("count"))

df_agg=df_kafka_string_formatted.groupBy(df_kafka_string_formatted.page).count()



df_kafka_string_formatted.printSchema()
df_agg.printSchema()
q=df_agg.writeStream.outputMode("update").format("delta").foreachBatch(upsertToDelta).start()
q.awaitTermination()