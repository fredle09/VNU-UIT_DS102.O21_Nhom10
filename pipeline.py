# import constants
from _constants import *

# import libs
import pandas as pd
import joblib

from preprocess import decoding_teencode, \
    remove_tag_icon_link, \
    remove_icon_punct_rendun_space, tokenization, \
    remove_stop_word, text_normalize
from transform import word_to_vector


class Pipeline:
    def __init__(self) -> None:
        pass

    def __preprocess(
        self,
        X: pd.DataFrame
    ) -> pd.DataFrame:
        X_copy: pd.DataFrame = X.copy()

        # decoding teencode
        X_copy = X_copy.applymap(decoding_teencode)
        print("Encoding Teencode:", X_copy.head(5), sep="\n", end="\n\n")

        # # remove tag-name, icon, link
        # X_copy = X_copy.applymap(remove_tag_icon_link)
        # print("Remove tag-name, icon, link:",
        #       X_copy.head(5), sep="\n", end="\n\n")

        # tokenization
        X_copy = X_copy.applymap(tokenization)
        print("Tokenizatioin:", X_copy.head(5), sep="\n", end="\n\n")

        # remove icon, punct, rendun space
        X_copy = X_copy.applymap(remove_icon_punct_rendun_space)
        print("Remove icon, punct, rendun space:",
              X_copy, sep="\n", end="\n\n")

        # lower case
        X_copy = X_copy.applymap(lambda x: x.lower())
        print("Lower:", X_copy.head(5), sep="\n", end="\n\n")

        # # remove stop word
        # X_copy = X_copy.applymap(remove_stop_word)
        # print("Remove stop Word:", X_copy.head(5), sep="\n", end="\n\n")

        # normalize text
        X_copy = X_copy.applymap(text_normalize)
        print("Normalize text:", X_copy.head(5), sep="\n", end="\n\n")

        return X_copy

    def __transform(
        self,
        X: pd.DataFrame
    ) -> str:
        X_copy: pd.DataFrame = X.copy()
        X_copy = X_copy.applymap(word_to_vector)
        return X_copy

    def __load_pretrained_model(
        self,
        model_name: str
    ) -> joblib:
        if model_name.lower() not in MODEL_NAME_LIST:
            raise ValueError(f"Model name {model_name} is not supported.")

        return joblib.load(MODEL_PATH.format(model_name))

    def run(
        self,
        X: pd.DataFrame
    ) -> pd.DataFrame:
        # Preprocess
        X_preprocessed: pd.DataFrame = self.__preprocess(X)

        # Word to vector
        X_transformed: pd.DataFrame = self.__transform(X_preprocessed)

        # Load model
        model: joblib = self.__load_pretrained_model("random_forest_model")

        # Predict
        y_pred: pd.DataFrame = model.predict(X_transformed)

        return y_pred

    def test(
        self,
        sentence: str
    ):
        df_test: pd.DataFrame = pd.DataFrame([sentence], columns=["sentence"])
        return self.__preprocess(df_test)

    # def test(
    #     self,
    #     X: pd.DataFrame
    # ):
    #     return self.__preprocess(X)


if __name__ == "__main__":
    pipeline = Pipeline()

    sentence: str = "Tôi là Nguyễn Khắc Trúc."
    print(sentence)
    print(pipeline.test(sentence))
    # df: pd.DataFrame = pd.read_csv(
    #     "./datasets/youtube_dataset_pbvm.csv", header=0)
    # # print(df["text"])

    # pipeline.test(df[['text']].sample(10))
