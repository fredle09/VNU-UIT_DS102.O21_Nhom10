# import constants
from _constants import *
import os

# import libs
import py_vncorenlp


class VnCoreNLP:
    __instance = None

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_instance():
        if VnCoreNLP.__instance is None:
            VnCoreNLP.__instance = py_vncorenlp.VnCoreNLP(
                annotators=["wseg"],
                save_dir=os.path.join(PATH, "VnCoreNLP/"),
            )
        return VnCoreNLP.__instance
