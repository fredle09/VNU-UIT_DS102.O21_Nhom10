"""
Store package
"""

# import libs
from pymongo.mongo_client import MongoClient

# import constants
from _constants import *


class MongoDB:
    """
    MongoDB class
    """

    __db = None

    def __new__(cls, url: str, db_name: str):
        if cls.__db is None:
            client = MongoClient(url)

            try:
                client.admin.command('ping')
                print("You successfully connected to MongoDB!")

                cls.__db = client[db_name]
            except Exception as err:
                print(err)
                cls.__db = None

        return cls.__db
