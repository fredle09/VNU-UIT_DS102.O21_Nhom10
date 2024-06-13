# import constants
from _constants import *

# import libs
import re
import gensim
import os
from underthesea import text_normalize

from _utils import VnCoreNLP


def decoding_teencode(sentence: str):
    words = sentence.split()
    replace_words = [
        TEENCODE_DICT.get(word, word)
        for word in words
    ]
    sententce_after_replaced: str = " ".join(replace_words)

    return sententce_after_replaced


def remove_tag_icon_link(sentence: str):
    sententce_after_replaced: str = re.sub(
        r'[@,#]\w+\b',
        '',
        sentence
    )

    return sententce_after_replaced


def remove_icon_punct_rendun_space(sentence: str):
    words: list[str] = gensim.utils.simple_preprocess(sentence)
    sentence_after_replaced: str = " ".join(words)

    return sentence_after_replaced


def tokenization(sentences: str):
    rdrsegmenter = VnCoreNLP.get_instance()

    sentence_lst: list[str] = rdrsegmenter.word_segment(sentences)
    res_sentences: str = " ".join(sentence_lst)

    return res_sentences


def remove_stop_word(sentence: str):
    words: list[str] = [word for word in sentence.split() if word.lower()
                        not in STOP_WORDS]
    sentence_after_removed: str = ' '.join(words)
    sentence_after_removed = sentence_after_removed.strip().lower()

    return sentence_after_removed
