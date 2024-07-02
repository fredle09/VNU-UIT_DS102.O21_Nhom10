"""
Declare all constants in this file
"""

# import libs
import os
import pandas as pd


PATH: str = os.path.dirname(os.path.abspath(__file__))

DELAY: int = 5

CAPTURE_TOPIC: str = "capture"

KAFKA_BROKER_SERVER: str = "localhost:9092"

MODEL_NAME_DICT = {
    "PhoBERT": "vinai/phobert-base",
    "BERTBase": "google-bert/bert-base-multilingual-cased",
}
MODEL_PATH: str = os.path.join(PATH, "trained_models/{}/tf_model.h5")

YOUTUBE_URL_COMMENT_FORMAT = "https://www.youtube.com/watch?v={}&lc={}"

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
    "vn": "Việt Nam",
    "TQ": "Trung Quốc",
    "sg": "Thành phố Hồ Chí Minh",
    "xh": "xã hội",
    "m": "mày",
    "bn": "bạn",
    "pbvm": "phân biệt vùng miền",
    "dm": "đ*t mẹ",
    "dmm": "đ* mẹ mày",
    "mxh": "mạng xã hội",
    "gđ": "gia đình",
    "kipo": "keo kiệt",
    "gato": "ganh tị",
}

STOP_WORDS_WITHOUT_DASH: list[str] = (
    pd
    .read_csv(
        os.path.join(PATH, "vietnamese-stopwords.txt"),
        dtype=str,
        encoding="utf-8",
        header=None,
    )
    .iloc[:, 0]
    .to_list()
)
print(STOP_WORDS_WITHOUT_DASH)

STOP_WORDS_WITH_DASH: list[str] = (
    pd
    .read_csv(
        os.path.join(PATH, "vietnamese-stopwords-dash.txt"),
        encoding="utf-8",
        header=None,
    )
    .iloc[:, 0]
    .to_list()
)

print(STOP_WORDS_WITH_DASH)
