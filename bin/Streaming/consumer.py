# import libs
from kafka import KafkaConsumer
import json

# import constants
from _constants import *


class Consumer:
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
    def __safe_json_loads(x):
        try:
            return json.loads(x.decode('utf-8'))
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print(f"Raw data: {x}")
            print("---")
            return None

    def get_message(
        self,
        key: Optional[str] = None,
    ):
        for message in self.__consumer:
            if key is not None and message.key != key:
                continue

            yield {
                "key": message.key,
                "value": message.value,
            }
