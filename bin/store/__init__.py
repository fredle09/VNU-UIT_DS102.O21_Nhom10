# import libs
from _constants import *
from pymongo.mongo_client import MongoClient


MONGODB_ATLAS_URL = os.getenv('MONGODB_ATLAS_URL')
if MONGODB_ATLAS_URL is None:
    raise ValueError("MONGODB_ATLAS_URL is not set")
MONGODB_ATLAS_DB_NAME = os.getenv('MONGODB_ATLAS_DB_NAME')
if MONGODB_ATLAS_DB_NAME is None:
    raise ValueError("MONGODB_ATLAS_DB_NAME is not set")


class MongoDB:
    __db = None

    def __new__(cls):
        if not cls.__db:
            client = MongoClient(MONGODB_ATLAS_URL)

            try:
                client.admin.command('ping')
                print("You successfully connected to MongoDB!")

                cls.__db = client[MONGODB_ATLAS_DB_NAME]
            except Exception as e:
                print(e)
                cls.__db = None

        return cls.__db
