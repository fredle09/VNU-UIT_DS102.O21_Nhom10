# import constants
from _constants import *
import os

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
    __instance: dict[str, Any] = {}

    def __new__(cls, model_name: str):
        if model_name.lower() not in MODEL_NAME_LIST:
            raise ValueError(f"{model_name} must in {MODEL_NAME_LIST}")

        if model_name not in cls.__instance.keys():
            cls.__instance[model_name] = joblib.load(
                MODEL_PATH.format(model_name))

        return cls.__instance[model_name]
