
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from kafka import KafkaConsumer

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
                        .add("count", LongType())

df_kafka_string_parsed=df_kafka_string.select(from_json(df_kafka_string.value,df_schema).alias("df_data"))

df_kafka_string_formatted=df_kafka_string_parsed.select(
        col("df_data.page").alias("page"),
        col("df_data.count").alias("count"))

df_kafka_string_formatted.printSchema()
