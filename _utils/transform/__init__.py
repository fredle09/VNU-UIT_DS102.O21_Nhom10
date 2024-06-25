# import constants
from _constants import *

# import utils
from _utils import LoadModel


def word_to_vector(series: pd.Series) -> pd.Series:
    model = LoadModel("text_vectorizer")
    return model.transform(series)
