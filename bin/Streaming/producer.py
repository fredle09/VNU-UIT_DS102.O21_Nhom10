# import lib
import sys

# import types
from typing import Optional

# import libs
import os
import csv
import json
from time import sleep
from datetime import datetime
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from kafka import KafkaProducer
from pyspark.sql import functions as F

# import constants
from _constants import *


class Producer:
    """
    A class to produce data to Kafka.
    """

    def __init__(
        self,
        topic: str,
        schema_list: list[str],
        csv_file_path: Optional[str] = None,
        spark_session: Optional[SparkSession] = None,
    ):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_SERVER,
            value_serializer=lambda v: str(v).encode("utf-8"),
        )
        self.spark_session: Optional[SparkSession] = spark_session
        self.topic: str = topic
        self.csv_file_path: Optional[str] = csv_file_path
        self.schema_list: list[str] = schema_list
        self.schema_data_types: dict[str, any] = dict()
        for col_info in schema_list:
            col_name, col_type = col_info.split(" ", 1)
            if col_type.lower() == "int":
                self.schema_data_types[col_name] = int
            elif col_type.lower() == "float":
                self.schema_data_types[col_name] = float
            elif col_type.lower() == "timestamp":
                self.schema_data_types[col_name] = datetime
            elif col_type.lower() == "boolean":
                self.schema_data_types[col_name] = bool
            else:
                self.schema_data_types[col_name] = str

    def store_csv_to_kafka(self, csv_file_path: str):
        """
        Reads a CSV file using the Spark session and stores the data to Kafka.

        Raises:
            Exception: If CSV file path is not provided
            FileNotFoundError: If the file is not found
            Exception: If Spark session is not provided
        """
        if not self.csv_file_path:
            raise Exception("CSV file path is not provided")
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"File not found: {csv_file_path}")
        if not self.spark_session:
            raise Exception("Spark session is not provided")

        df: DataFrame = self.spark_session.read.csv(
            paht=csv_file_path,
            schema=" ".join(self.schema_list),
        )

        return self.store_dataframe_to_kafka(df)

    def store_dataframe_to_kafka(self, df: DataFrame):
        """
        Stores the data from a DataFrame to Kafka.

        Raises:
            Exception: If DataFrame is not provided
        """
        sql_exprs = ["to_json(struct(*)) AS value"]

        # Apply the date_format function to each timestamp column
        df = df.withColumns(
            {
                col_name: F.date_format(col_name, "yyyy-MM-dd HH:mm:ss")
                # Timestamp columns are in the format "yyyy-MM-dd HH:mm:ss"
                for col_name in [
                    col[0] for col in df.dtypes if "timestamp" in col[1].lower()
                ]
            }
        )

        return (
            df.selectExpr(*sql_exprs)
            .write.format("kafka")
            .option("kafka.bootstrap.servers", KAFKA_BROKER_SERVER)
            .option("topic", self.topic)
            .save()
        )

    def __convert_str_to_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        """
        Converts a string to a datetime object.

        Args:
            datetime_str (str): The datetime string to convert

        Returns:
            Optional[datetime]: The datetime object or None if the string is empty
        """
        if not datetime_str:
            return None
        return datetime.strptime(datetime_str, DATETIME_FORMAT)

    def __get_time_diff(self, datetime_1: datetime, datetime_2: datetime) -> float:
        """
        Calculates the difference between two datetime objects.

        Args:
            datetime_1 (datetime): The first datetime object
            datetime_2 (datetime): The second datetime object

        Returns:
            float: The difference in seconds
        """
        return (datetime_1 - datetime_2).total_seconds()

    def __convert_data_types_of_record(self, record: dict) -> dict:
        """
        Converts the data types of the record values.

        Args:
            record (dict): The record to convert

        Returns:
            dict: The record with the converted data types
        """
        for col_name, col_type in self.schema_data_types.items():
            if col_type != datetime:
                record[col_name] = col_type(record[col_name])
            else:
                record[col_name] = self.__convert_str_to_datetime(
                    record[col_name]
                )

        return record

    def __send_to_kafka(self, record: dict) -> None:
        """
        Sends a record to Kafka.

        Args:
            record (dict): The record to send
        """
        for key, value in record.items():
            if type(value) == datetime:
                record[key] = value.strftime(DATETIME_FORMAT)

        record_in_json: str = json.dumps(record, indent=0, ensure_ascii=False)
        self.producer.send(self.topic, record_in_json)

    def streaming_data_to_kafka(self) -> None:
        """
        Streams data from a csv file to Kafka.
        """
        if not self.csv_file_path:
            raise Exception("CSV file path is not provided")
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"File not found: {self.csv_file_path}")

        with open(self.csv_file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=list(
                self.schema_data_types.keys()))

            # Skip the header
            next(reader)
            row: dict = next(reader)
            row = self.__convert_data_types_of_record(row)
            previous_time: Optional[datetime] = None
            # Set the first time point
            current_time: datetime = row["updated_at"]

            # Ensure that the first data is streamed at the start time
            if previous_time and current_time > previous_time:
                time_diff: float = self.__get_time_diff(
                    current_time, previous_time)
                sleep(time_diff * DELAY)

            # Streaming data from the current row
            while True:
                # Set time point to calculate the time to sleep
                time_point: datetime = datetime.now()

                # Handle the case where the next data has the same time as the
                # current data
                while True:
                    self.__send_to_kafka(row)

                    # Handle the case where the streaming all the data
                    try:
                        row = next(reader)
                        row = self.__convert_data_types_of_record(row)

                    except StopIteration:
                        print("Reached end of file")
                        return

                    # Break if the next data has the different time
                    if row["updated_at"] > current_time:
                        break

                # Update the previous time and current time
                previous_time = current_time
                current_time = row["updated_at"]

                # Sleep to simulate the real-time data stream
                diff_time: float = self.__get_time_diff(
                    current_time, previous_time
                )
                time_process: float = (
                    datetime.now() - time_point
                ).total_seconds()

                sleep(diff_time * DELAY - time_process)


def using_producer_for_streaming(csv_file_path: str) -> None:
    if not csv_file_path:
        raise Exception("CSV file path is not provided")
    elif not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"File not found: {csv_file_path}")

    pro: Producer = Producer(
        topic=CAPTURE_TOPIC,
        schema_list=CAPTURE_YOUTUBE_SCHEMA_LIST,
        csv_file_path=csv_file_path,
    )
    pro.streaming_data_to_kafka()


sys.modules[__name__] = Producer
