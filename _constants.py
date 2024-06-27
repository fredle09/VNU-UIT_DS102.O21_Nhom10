# import libs
import os

from time import sleep
from typing import Optional, Callable, Any

import pandas as pd
import numpy as np

import joblib

from dotenv import load_dotenv


# findspark.init()
load_dotenv()


PATH: str = os.path.dirname(os.path.abspath(__file__))

DELAY: int = 1

CAPTURE_TOPIC: str = "capture"

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
