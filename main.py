# import libs
import pandas as pd

# import constants
from _constants import *

# import bin
from bin.pipeline import Pipeline
from bin.store import MongoDB

# import _utils
from _utils import create_link_to_comment


def main():
    # pipe: Pipeline = Pipeline()
    # df: pd.DataFrame = pd.read_csv(
    #     "datasets/youtube_dataset_pbvm.csv",
    #     header=0
    # )
    # # print(df[["text"]])
    # # print(pipe.test(df[["text"]]))
    # df_preprocessed: pd.DataFrame = pipe.test(df[["text"]])
    # df_preprocessed.to_csv(
    #     os.path.join(
    #         PATH,
    #         "datasets",
    #         "youtube_dataset_pbvm_preprocessed.csv"
    #     ),
    #     index=False,
    #     header=True
    # )
    # print("Done")
    # MongoDB()
    # pred = Predict(
    #     platform="youtube",
    #     text="I love this video!",
    #     label=0
    # )

    # pred.save()
    # pipe = Pipeline()

    # X_raw: pd.DataFrame = pd.read_csv(
    #     "datasets/youtube_dataset_pbvm.csv",
    #     header=0
    # )

    # y_pred: pd.DataFrame = pipe.test(X_raw)
    # print(y_pred)

    # X: pd.DataFrame = pd.DataFrame([
    #     "T là thằng phân biệt vùng miền",
    #     "Miền bắc, miền nam là một",
    # ], columns=["text"])

    X_raw: pd.DataFrame = pd.read_csv(
        "datasets/2024_06_25_youtube_pbvm_Hieu.csv",
        header=0
    ).sample(50)
    pipe = Pipeline()
    X_preprocessed: pd.DataFrame = pipe.preprocess(X_raw)
    y_pred: pd.DataFrame = pipe.predict(
        X_preprocessed,
    )
    pred: pd.DataFrame = X_raw.join(y_pred)
    pred["platform"] = "youtube"
    pred["link"] = pred.apply(
        lambda row: create_link_to_comment(
            platform="youtube",
            video_id=row["video_id"],
            comment_id=row["comment_id"]
        ),
        axis=1
    )
    pred = pred[["platform", "text", "label", "link"]]
    dict_pred_list: list[dict] = pred.to_dict("records")

    database = MongoDB()
    database['predicts'].insert_many(dict_pred_list)
    ...


if __name__ == "__main__":
    main()
