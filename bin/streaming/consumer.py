"""
Consumer class for Kafka.
"""

# import type
from typing import Optional

# import libs
import json
from kafka import KafkaConsumer

# import constants
from _constants import KAFKA_BROKER_SERVER


class Consumer:
    """
    Kafka consumer class.
    """

    def __init__(
        self,
        topic: str,
    ):
        self.topic: str = topic
        self.__consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=KAFKA_BROKER_SERVER,
            auto_offset_reset="latest",
            enable_auto_commit=True,
            key_deserializer=lambda x: (
                x.decode('utf-8')
                if x is not None
                else None
            ),
            value_deserializer=lambda x: (
                Consumer.__safe_json_loads(x)
                if x is not None
                else None
            ),
        )

    @staticmethod
    def __safe_json_loads(data: bytes):
        """
        Safely load JSON data.

        Args:
            data (bytes): The JSON data.

        Returns:
            dict: The JSON data.
        """

        try:
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError as err:
            print(f"JSONDecodeError: {err}")
            print(f"Raw data: {data}")
            print("---")
            return None

    def get_message(
        self,
        key: Optional[str] = None,
    ):
        """
        Get a message from a Kafka topic.

        Args:
            key (Optional[str]): The key of the message.
        """
        for message in self.__consumer:
            if key is not None and message.key != key:
                continue

            yield {
                "key": message.key,
                "value": message.value,
            }
