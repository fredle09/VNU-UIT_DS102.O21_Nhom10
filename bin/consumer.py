# import types
from typing import Optional

# import libs
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# import constants
from _constants import *


class Consumer:
    def __init__(
        self,
        topic: str,
        schema_list: list[str],
        spark_session: SparkSession,
    ) -> None:
        self.topic: str = topic
        self.schema_list: list[str] = schema_list
        self.spark_session: SparkSession = spark_session

    def get_streaming_df(self) -> DataFrame:
        raw_streaming_df: DataFrame = (
            self.spark_session.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BROKER_SERVER)
            .option("subscribe", self.topic)
            .option("startingOffsets", "latest")
            .load()
        )

        streaming_df: DataFrame = (
            raw_streaming_df.selectExpr("CAST(value AS STRING)")
            .select(F.from_json("value", ", ".join(self.schema_list)).alias("data"))
            .selectExpr("data.*")
        )

        return streaming_df

    def get_history_df(
        self,
        from_timestamp: Optional[datetime] = None,
        timestamp_col: str = "updated_at"
    ) -> DataFrame:
        raw_history_df: DataFrame = (
            self.spark_session.read
            .format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BROKER_SERVER)
            .option("subscribe", self.topic)
            .option("startingOffsets", "earliest")
            .option("endingOffsets", "latest")
            .load()
        )

        history_df: DataFrame = (
            raw_history_df.tail(20).selectExpr("CAST(value AS STRING)")
            .select(F.from_json("value", ", ".join(self.schema_list)).alias("data"))
            .selectExpr("data.*")
        )

        if from_timestamp:
            if timestamp_col not in [
                col_type.split(" ")[0] for col_type in self.schema_list
            ]:
                raise ValueError(
                    f"The {timestamp_col} column is not in the {self.schema_list}.",
                )

            history_df = history_df.filter(
                F.col(timestamp_col) >= from_timestamp
            )

        return history_df
