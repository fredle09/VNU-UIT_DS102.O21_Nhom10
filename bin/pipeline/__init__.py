# import constants
from _constants import *

# import types
from typing import Any

# import libs
import pandas as pd
import joblib

from _utils.preprocess import decoding_teencode, \
    remove_tag_icon_link, \
    remove_icon_punct_rendun_space, tokenization, \
    remove_stop_word, text_normalize
from _utils.transform import word_to_vector


class Pipeline:
    def __init__(self):
        self.trained_model: Any = None

    def preprocess(
        self,
        X: pd.DataFrame,
        is_debug: bool = False
    ) -> pd.DataFrame:
        X_copy: pd.DataFrame = X.copy()
        if is_debug:
            print("Original:", X_copy.head(5), sep="\n", end="\n\n")

        # decoding teencode
        X_copy = X_copy.applymap(decoding_teencode)
        if is_debug:
            print("Encoding Teencode:", X_copy.head(5), sep="\n", end="\n\n")

        # # remove tag-name, icon, link
        # X_copy = X_copy.applymap(remove_tag_icon_link)
        # print("Remove tag-name, icon, link:",
        #       X_copy.head(5), sep="\n", end="\n\n")

        # tokenization
        X_copy = X_copy.applymap(tokenization)
        if is_debug:
            print("Tokenizatioin:", X_copy.head(5), sep="\n", end="\n\n")

        # # remove icon, punct, rendun space
        # X_copy = X_copy.applymap(remove_icon_punct_rendun_space)
        # print("Remove icon, punct, rendun space:",
        #       X_copy, sep="\n", end="\n\n")

        # lower case
        X_copy = X_copy.applymap(lambda x: x.lower())
        if is_debug:
            print("Lower:", X_copy.head(5), sep="\n", end="\n\n")

        # # remove stop word
        # X_copy = X_copy.applymap(remove_stop_word)
        # print("Remove stop Word:", X_copy.head(5), sep="\n", end="\n\n")

        # normalize text
        X_copy = X_copy.applymap(text_normalize)
        if is_debug:
            print("Normalize text:", X_copy.head(5), sep="\n", end="\n\n")

        return X_copy

    def transform(
        self,
        X: pd.DataFrame
    ) -> str:
        X_copy: pd.DataFrame = X.copy()
        X_copy = X_copy.applymap(word_to_vector)
        return X_copy

    def load_pretrained_model(
        self,
        model_name: str
    ) -> joblib:
        if model_name.lower() not in MODEL_NAME_LIST:
            raise ValueError(f"Model name {model_name} is not supported.")

        self.trained_model = joblib.load(MODEL_PATH.format(model_name))

        return self.trained_model

    def run(
        self,
        X: pd.DataFrame
    ) -> pd.DataFrame:
        # Preprocess
        X_preprocessed: pd.DataFrame = self.preprocess(X)

        # Word to vector
        X_transformed: pd.DataFrame = self.transform(X_preprocessed)

        # Load model
        model: joblib = self.load_pretrained_model("random_forest_model")

        # Predict
        y_pred: pd.DataFrame = model.predict(X_transformed)

        return y_pred

    def test(
        self,
        X: pd.DataFrame,
    ):
        X_preprocessed: pd.DataFrame = self.preprocess(X)
        return X_preprocessed
