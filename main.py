# import libs
import pandas as pd

# import constants
from _constants import *

# import bin
from bin.pipeline import Pipeline


def main():
    pipe: Pipeline = Pipeline()
    df: pd.DataFrame = pd.read_csv(
        "datasets/youtube_dataset_pbvm.csv",
        header=0
    )
    # print(df[["text"]])
    # print(pipe.test(df[["text"]]))
    df_preprocessed: pd.DataFrame = pipe.test(df[["text"]])
    df_preprocessed.to_csv(
        os.path.join(PATH, "datasets", "youtube_dataset_pbvm_preprocessed.csv"),
        index=False,
        header=True
    )
    print("Done")


if __name__ == "__main__":
    main()
