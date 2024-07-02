"""
This script consumes messages from Kafka, predicts the sentiment of the message and stores
the data in MongoDB.
"""

# import types
from typing import Any

# import libs
import os
import sys
import threading
from time import sleep
from dotenv import load_dotenv
import pandas as pd

# import bin
from bin.streaming.consumer import Consumer
from bin.pipeline import Pipeline
from bin.store import MongoDB

# import _utils
from _utils import create_link_to_comment

# import constants
from _constants import CAPTURE_TOPIC


load_dotenv()

DATA_BUCKET: list[Any] = []

MONGODB_ATLAS_URL = os.getenv('MONGODB_ATLAS_URL')
if MONGODB_ATLAS_URL is None:
    raise ValueError("MONGODB_ATLAS_URL is not set")
MONGODB_ATLAS_DB_NAME = os.getenv('MONGODB_ATLAS_DB_NAME')
if MONGODB_ATLAS_DB_NAME is None:
    raise ValueError("MONGODB_ATLAS_DB_NAME is not set")


def consume_messages():
    """
    Consume messages from Kafka.
    """

    global DATA_BUCKET

    con: Consumer = Consumer(
        topic=CAPTURE_TOPIC,
    )

    try:
        for message in con.get_message():
            platform = message["key"]
            data = message["value"]
            DATA_BUCKET.append({"platform": platform, **data})
            print("Data received...")
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


def predict_and_store():
    """
    Predict the sentiment of the message and store the data in MongoDB.
    """

    global DATA_BUCKET

    pipe: Pipeline = Pipeline()

    database = MongoDB(
        url=MONGODB_ATLAS_URL,
        db_name=MONGODB_ATLAS_DB_NAME,
    )

    i = 0

    try:
        while True:
            if len(DATA_BUCKET) != 0:
                local_data_bucket = DATA_BUCKET
                DATA_BUCKET = []  # clear data_bucket

                df_raw: pd.DataFrame = pd.DataFrame(local_data_bucket)
                y_pred: pd.Series = pipe.run(df_raw)
                df_predict: pd.DataFrame = df_raw.join(y_pred)
                df_predict["link"] = (
                    df_predict
                    .apply(create_link_to_comment, axis=1)
                )
                df_predict_to_records = df_predict.to_dict(orient="records")
                database["predicts"].insert_many(df_predict_to_records)
                print("Predicted and stored data...")

                i += 1
            else:
                print("No data to predict")
            sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consume_messages)
    predict_thread = threading.Thread(target=predict_and_store)

    threads = [
        consumer_thread,
        predict_thread
    ]

    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
