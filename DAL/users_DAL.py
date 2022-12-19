from pymongo import MongoClient
from bson import ObjectId
# from test import mongourl
from dotenv import load_dotenv
load_dotenv()
import os

SECRET_URI = os.getenv("MONGOURI")

class UsersDAL:
    def __init__(self):
        self._client = MongoClient(SECRET_URI)
        self._db = self._client["factoryDB"]
        self._collection = self._db["users"]

    def get_users(self):
        users = list(self._collection.find({}))
        return users
