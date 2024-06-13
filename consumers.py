# import libs
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from bin.consumer import Consumer

# import constants
from _constants import *

import findspark
findspark.init()

if __name__ == '__main__':
    spark_session: SparkSession = (
        SparkSession.builder
        .master("local[*]")
        .appName("Kafka-Streaming")
        .config("spark.jars.packages", ",".join(SPARK_STREAMING_PACKAGES))
        .config("spark.sql.streaming.schemaInference", "true")
        .getOrCreate()
    )

    con: Consumer = Consumer(
        topic=CAPTURE_TOPIC,
        schema_list=CAPTURE_YOUTUBE_SCHEMA_LIST,
        spark_session=spark_session
    )

    streaming_df: DataFrame = con.get_streaming_df()
    query: StreamingQuery = streaming_df.writeStream.format("console").start()
    query.awaitTermination()
