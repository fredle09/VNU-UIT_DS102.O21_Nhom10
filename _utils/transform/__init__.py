# import constants
from _constants import *

# import utils
from _utils import LoadModel


def word_to_vector(word: str) -> joblib:
    model = LoadModel("text_vectorizer")
    return model.transform(word)
