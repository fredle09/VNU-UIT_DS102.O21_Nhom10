# import libs
import re
import gensim
from underthesea import text_normalize

# import utils
from _utils import VnCoreNLP

# import constants
from _constants import *


def decoding_teencode(sentence: str):
    # print(">> sentence:", sentence, end="\n\n")
    # if not isinstance(sentence, str):
    #     sentence = str(sentence)
    try:
        words = sentence.split()
        replace_words = [
            TEENCODE_DICT.get(word, word)
            for word in words
        ]
        sententce_after_replaced: str = " ".join(replace_words)

        return sententce_after_replaced
    except Exception as e:
        print(f"Have error {e} with sentence: {sentence}")
        return ''


def remove_tag_icon_link(sentence: str):
    try:
        sententce_after_replaced: str = re.sub(
            r'[@,#]\w+\b',
            '',
            sentence
        )
        return sententce_after_replaced
    except Exception as e:
        print(f"Have error {e} with sentence: {sentence}")
        return ''


def remove_icon_punct_rendun_space(sentence: str):
    words: list[str] = gensim.utils.simple_preprocess(sentence)
    sentence_after_replaced: str = " ".join(words)

    return sentence_after_replaced


def tokenization(sentences: str):
    rdrsegmenter = VnCoreNLP()

    sentence_lst: list[str] = rdrsegmenter.word_segment(sentences)
    res_sentences: str = " ".join(sentence_lst)

    return res_sentences


def remove_stop_word(sentence: str, with_dash: bool = False):
    STOP_WORDS: list[str] = STOP_WORDS_WITH_DASH if with_dash else STOP_WORDS_WITHOUT_DASH
    words: list[str] = [word for word in sentence.split() if word.lower()
                        not in STOP_WORDS]
    sentence_after_removed: str = ' '.join(words)
    sentence_after_removed = sentence_after_removed.strip().lower()

    return sentence_after_removed
