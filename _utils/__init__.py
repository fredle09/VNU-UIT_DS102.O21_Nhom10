# import constants
from _constants import *
import os

# import libs
import py_vncorenlp


class VnCoreNLP:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = py_vncorenlp.VnCoreNLP(
                annotators=["wseg"],
                save_dir=os.path.join(PATH, "VnCoreNLP/"),
            )

        return cls.__instance
