# import libs
from _constants import *
from pymongo.mongo_client import MongoClient
from pymongoose.mongo_types import Types, Schema
from pymongoose.methods import set_schemas


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
                schemas = {
                    model.schema_name: model(empty=True).schema
                    for model in [Predict]
                }
                set_schemas(cls.__db, schemas)
            except Exception as e:
                print(e)
                cls.__db = None

        return cls.__db


class Predict(Schema):
    schema_name = "predicts"  # Name of the schema that mongo uses

    _id = None
    platform: str
    text: str
    label: int
    link: str

    def __init__(self, **kwargs):
        self.schema = {
            "platform": {"type": Types.String, "required": True},
            "text": {"type": Types.String, "required": True},
            "label": {"type": Types.Number, "required": True},
            "link": {"type": Types.String, "required": False},
        }

        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self):
        return f"platform: {self.platform}, text: {self.name}, label: {self.label}"
