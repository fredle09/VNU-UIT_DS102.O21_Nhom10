"""
Pipeline package
"""

# import types
from typing import Any

# import libs
import pandas as pd

# import constants
from _constants import *

# import _utils
from _utils.preprocess import decoding_teencode, \
    remove_tag_icon_link, \
    remove_icon_punct_rendun_space, segmentation, \
    text_normalize
from _utils import LoadModel


class Pipeline:
    """
    Pipeline class.
    """

    def __init__(self, model_name: str = "BERTBase"):
        self.model_name: Any = model_name

    def preprocess(
        self,
        x_test: pd.DataFrame,
        input_col: str = "text",
        is_debug: bool = False
    ) -> pd.DataFrame:
        """
        Preprocess the data.

        Args:
            x_test (pd.DataFrame): The data to preprocess.
            input_col (str): The input column.
            is_debug (bool): Debug mode.

        Returns:
            pd.DataFrame: The preprocessed data.
        """
        if input_col not in x_test.columns:
            raise ValueError(f"Column {input_col} not found in DataFrame")

        output_col: str = f"{input_col}__preprocessed"
        input_col: str = f"{input_col}"
        x_copy: pd.DataFrame = x_test.copy()
        x_copy[output_col] = x_copy[input_col]
        if is_debug:
            print("Original:", x_copy.head(5), sep="\n", end="\n\n")

        # remove tag-name, icon, link
        x_copy = x_copy.applymap(remove_tag_icon_link)
        if is_debug:
            print("Remove tag-name, icon, link:",
                  x_copy.head(5), sep="\n", end="\n\n")

        # remove icon, punct, rendun space
        x_copy = x_copy.applymap(remove_icon_punct_rendun_space)
        if is_debug:
            print("Remove icon, punct, rendun space:",
                  x_copy, sep="\n", end="\n\n")

        # lower case
        x_copy[output_col] = x_copy[output_col].map(lambda x: x.lower())
        if is_debug:
            print("Lower:", x_copy.head(5), sep="\n", end="\n\n")

        # tokenization
        x_copy[output_col] = x_copy[output_col].map(segmentation)
        if is_debug:
            print("Tokenizatioin:", x_copy.head(5), sep="\n", end="\n\n")

        # normalize text
        x_copy[output_col] = x_copy[output_col].map(text_normalize)
        if is_debug:
            print("Normalize text:", x_copy.head(5), sep="\n", end="\n\n")

        # decoding teencode
        x_copy[output_col] = x_copy[output_col].map(decoding_teencode)
        if is_debug:
            print(
                "Encoding Teencode:",
                x_copy[output_col].head(5), sep="\n", end="\n\n"
            )

        return x_copy

    def predict(
        self,
        x_test: pd.DataFrame,
        input_col: str = "text",
    ) -> pd.Series:
        """
        Predict the data.

        Args:
            x_test (pd.DataFrame): The data to predict.
            input_col (str): The input column.

        Returns:
            pd.Series: The predicted data.
        """

        input_col: str = f"{input_col}__preprocessed"
        if input_col not in x_test.columns:
            raise ValueError(f"Column {input_col} not found in DataFrame")

        x_copy: pd.DataFrame = x_test.copy()

        model = LoadModel(self.model_name)
        y_pred = x_copy[input_col].apply(model.predict)

        y_pred.name = "pred"
        return y_pred

    def run(
        self,
        x_run: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Run the pipeline.

        Args:
            x_run (pd.DataFrame): The data to run the pipeline.

        Returns:
            pd.DataFrame: The predicted data.
        """

        # Preprocess
        x_preprocessed: pd.DataFrame = self.preprocess(x_run)

        # Predict
        y_pred: pd.DataFrame = self.predict(
            x_preprocessed,
        )

        return y_pred

    def test(
        self,
        x_test: pd.DataFrame,
    ):
        """
        Test the pipeline.

        Args:
            x_test (pd.DataFrame): The test data.

        Returns:
            pd.DataFrame: The preprocessed data.
        """
        x_preprocessed: pd.DataFrame = self.preprocess(x_test, is_debug=True)
        return x_preprocessed
