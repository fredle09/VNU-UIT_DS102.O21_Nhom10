"""
Producer class
"""

# import type
from typing import Any, Optional

# import libs
import os
import random
import json
import csv
from time import sleep
from kafka import KafkaProducer

# import constants
from _constants import KAFKA_BROKER_SERVER, PATH, DELAY


class Producer:
    """
    Kafka producer class.
    """

    __producer: Optional[KafkaProducer] = None

    def __init__(
        self,
        topic: str,
    ) -> None:
        """
        Initialize the Kafka producer.
        """

        if not Producer.__producer:
            Producer.__producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER_SERVER,
                key_serializer=lambda k: str(k).encode("utf-8")if k else None,
                value_serializer=lambda v: json.dumps(
                    v,
                    ensure_ascii=False
                ).encode("utf-8"),
            )

        self.topic: str = topic

    def send_message(
        self,
        key: str,
        value: Any,
    ):
        """
        Send a message to a Kafka topic.
        """

        Producer.__producer.send(
            topic=self.topic,
            key=key,
            value=value
        )
        Producer.__producer.flush()

    def send_message_from_csv(
        self,
        csv_file_path: str,
    ) -> None:
        """
        Send messages from a CSV file to a Kafka topic.
        """

        full_path: str = os.path.join(
            PATH,
            "datasets",
            csv_file_path
        )

        type_of_data: str = csv_file_path.split("_")[0]

        with open(full_path, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                Producer.__producer.send(
                    topic=self.topic,
                    key=type_of_data,
                    value=row
                )

                Producer.__producer.flush()
                # print({"topic": self.topic, "key": type_of_data, "value": row})
                time_to_sleep: float = random.random() * DELAY + DELAY / 2
                sleep(time_to_sleep)
