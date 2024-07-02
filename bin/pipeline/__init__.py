# import constants
from _constants import *

# import types
from typing import Any

# import libs
import pandas as pd

# import _utils
from _utils.preprocess import decoding_teencode, \
    remove_tag_icon_link, \
    remove_icon_punct_rendun_space, tokenization, \
    remove_stop_word, text_normalize
from _utils.transform import word_to_vector
from _utils import LoadModel


class Pipeline:
    def __init__(self, model_name: str = "BERTBase"):
        self.model_name: Any = model_name

    def preprocess(
        self,
        X: pd.DataFrame,
        input_col: str = "text",
        is_debug: bool = False
    ) -> pd.DataFrame:
        if input_col not in X.columns:
            raise ValueError(f"Column {input_col} not found in DataFrame")

        output_col: str = f"{input_col}__preprocessed"
        input_col: str = f"{input_col}"
        X_copy: pd.DataFrame = X.copy()
        X_copy[output_col] = X_copy[input_col]
        if is_debug:
            print("Original:", X_copy.head(5), sep="\n", end="\n\n")

        # remove tag-name, icon, link
        X_copy = X_copy.applymap(remove_tag_icon_link)
        if is_debug:
            print("Remove tag-name, icon, link:",
                  X_copy.head(5), sep="\n", end="\n\n")

        # remove icon, punct, rendun space
        X_copy = X_copy.applymap(remove_icon_punct_rendun_space)
        if is_debug:
            print("Remove icon, punct, rendun space:",
                  X_copy, sep="\n", end="\n\n")

        # lower case
        X_copy[output_col] = X_copy[output_col].map(lambda x: x.lower())
        if is_debug:
            print("Lower:", X_copy.head(5), sep="\n", end="\n\n")

        # tokenization
        X_copy[output_col] = X_copy[output_col].map(tokenization)
        if is_debug:
            print("Tokenizatioin:", X_copy.head(5), sep="\n", end="\n\n")

        # normalize text
        X_copy[output_col] = X_copy[output_col].map(text_normalize)
        if is_debug:
            print("Normalize text:", X_copy.head(5), sep="\n", end="\n\n")

        # decoding teencode
        X_copy[output_col] = X_copy[output_col].map(decoding_teencode)
        if is_debug:
            print("Encoding Teencode:",
                  X_copy[output_col].head(5), sep="\n", end="\n\n")

        return X_copy

    def predict(
        self,
        X: pd.DataFrame,
        input_col: str = "text",
    ) -> pd.Series:
        input_col: str = f"{input_col}__preprocessed"
        if input_col not in X.columns:
            raise ValueError(f"Column {input_col} not found in DataFrame")

        X_copy: pd.DataFrame = X.copy()

        model = LoadModel(self.model_name)
        y_pred = X_copy[input_col].apply(model.predict)

        y_pred.name = "pred"
        return y_pred
        ...

    def run(
        self,
        X: pd.DataFrame,
    ) -> pd.DataFrame:
        # Preprocess
        X_preprocessed: pd.DataFrame = self.preprocess(X)

        # Predict
        y_pred: pd.DataFrame = self.predict(
            X_preprocessed,
        )

        return y_pred

    def test(
        self,
        X: pd.DataFrame,
    ):
        X_preprocessed: pd.DataFrame = self.preprocess(X, is_debug=True)
        return X_preprocessed
