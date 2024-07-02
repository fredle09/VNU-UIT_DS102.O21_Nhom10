# import constants
from _constants import *
import os
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

# import libs
import py_vncorenlp


def create_link_to_comment(row: dict) -> str:
    YOUTUBE_URL_COMMENT_FORMAT = "https://www.youtube.com/watch?v={}&lc={}"
    platform: str = row.get("platform")
    if platform is None:
        raise ValueError("platform must be a column")

    if platform == "youtube":
        video_id: str = row.get("video_id")
        comment_id: str = row.get("comment_id")
        if video_id is None or comment_id is None:
            raise ValueError("video_id and comment_id must be columns")
        return YOUTUBE_URL_COMMENT_FORMAT.format(video_id, comment_id)

    if platform == "reddit":
        return row.get("comment_link")

    if platform == "tiktok":
        return None
    ...


class VnCoreNLP:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = py_vncorenlp.VnCoreNLP(
                annotators=["wseg"],
                save_dir=os.path.join(PATH, "VnCoreNLP/"),
            )

        return cls.__instance


class LoadModel:
    __instance = None

    def __new__(cls, model_name: str):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.model_name = model_name
            cls.__instance._initialize(model_name)
        return cls.__instance

    def _initialize(self, model_name: str):
        if model_name not in MODEL_NAME_DICT.keys():
            raise ValueError("Model name not found in the dictionary")

        self.__instance = {}
        self.__instance["model"] = TFBertForSequenceClassification.from_pretrained(
            MODEL_NAME_DICT[model_name],
            num_labels=3
        )

        self.__instance["model"].load_weights(
            MODEL_PATH.format(model_name)
        )

        self.__instance["tokenizer"] = BertTokenizer.from_pretrained(
            MODEL_NAME_DICT[model_name]
        )

    def predict(self, input_text: str) -> int:
        if (self.__instance["tokenizer"] is None
                or self.__instance["model"] is None):
            self._initialize(self._instance.model_name)

        inputs = self.__instance["tokenizer"](
            input_text, return_tensors="tf",
            padding=True, truncation=True
        )

        logits = self.__instance["model"](inputs).logits
        probabilities = tf.nn.softmax(logits, axis=-1)
        predicted_class_index = tf.argmax(probabilities, axis=-1).numpy()[0]
        return predicted_class_index
