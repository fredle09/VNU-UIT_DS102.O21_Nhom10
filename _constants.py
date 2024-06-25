# import libs
import threading
import findspark
from pyspark.sql.streaming.query import StreamingQuery
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import os

from time import sleep, time
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

import pandas as pd
import numpy as np

import joblib

from dotenv import load_dotenv


findspark.init()
load_dotenv()


PATH: str = os.path.dirname(os.path.abspath(__file__))

DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"

SCALA_VERSION: str = "2.12"
SPARK_VERSION: str = "3.5.1"
KAFKA_VERSION: str = "3.7.0"

DELAY: int = 1

SPARK_STREAMING_PACKAGES: list[str] = [
    f"org.apache.spark:spark-sql-kafka-0-10_{SCALA_VERSION}:{SPARK_VERSION}",
    f"org.apache.kafka:kafka-clients:{KAFKA_VERSION}"
]

KAFKA_BROKER_SERVER: str = "localhost:9092"

CAPTURE_TOPIC: str = "capture"
CAPTURE_YOUTUBE_SCHEMA_LIST: list[str] = [
    "idx INT",
    "author STRING",
    "updated_at TIMESTAMP",
    "like_count INT",
    "text STRING",
    "video_id STRING",
    "public BOOLEAN"
]

MODEL_NAME_LIST: list[str] = [
    "random_forest_model",
    "text_vectorizer"
]

MODEL_PATH: str = os.path.join(PATH, "trained_models/{}.joblib")

TEENCODE_DICT: dict[str, str] = {
    "t": "tôi",
    "K": "không",
    "k": "không",
    "ko": "không",
    "nhma": "nhưng mà",
    "b": "bạn",
    "h": "giờ",
    "z": "vậy",
    "v": "vậy",
    "ng": "người",
    "ngta": "người ta",
    "mn": "mọi người",
    "ms": "mới",
    "dc": "được",
    "đc": "được",
    "r": "rồi",
    "bl": "bình luận",
    "vk": "vợ",
    "ck": "chồng",
    "thg": "thằng",
    "CA": "công an",
    "th": "thằng",
    "e": "em",
    "vs": "với",
    "ae": "anh em",
    "ntn": "như thế này",
    "bt": "biết",
    "j": "gì",
    "cgi": "cái gì",
    "fb": "facebook",
    "cmt": "bình luận",
    "tks": "cảm ơn",
    "dt": "dân tộc",
    "mb": "miền bắc",
    "mt": "miền trung",
    "mn": "miền nam",
    "vn": "Việt Nam",
    "TQ": "Trung Quốc",
    "sg": "Thành phố Hồ Chí Minh",
    "xh": "xã hội",
    "m": "mày",
    "bn": "bạn",
    # "Parky" : "bắc kỳ",
    # "parky" : "bắc kỳ",
    # "pảky" : "bắc kỳ",
    # "packy" : "bắc kỳ",
    # "baki" : "bắc kỳ",
    # "namki" : "nam kỳ",
    # "namky" : "nam kỳ",
    # "namkiki" : "nam kỳ",
    # "nameky" : "nam kỳ",
    # "naki" : "nam kỳ",
    "pbvm": "phân biệt vùng miền",
    "dm": "đ*t mẹ",
    "dmm": "đ* mẹ mày",
    "mxh": "mạng xã hội",
    "gđ": "gia đình",
    "kipo": "keo kiệt",
    "gato": "ganh tị",
}

# https://github.com/stopwords/vietnamese-stopwords?tab=readme-ov-file#license
# STOP_WORDS: list[str] = []
# with open(
#     "./vietnamese-stopwords-dash.txt",
#     mode='r',
#     encoding="utf-8"
# ) as f:
#     if len(STOP_WORDS) == 0:
#         STOP_WORDS.extend(f.read().splitlines())

DATABASE_NAME = 'DS102.O21_GROUP10'
