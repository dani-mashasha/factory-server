from pymongo import MongoClient
from bson import ObjectId
# from test import mongourl
from dotenv import load_dotenv
load_dotenv()
import os

SECRET_URI = os.getenv("MONGOURI")

class ShiftsDAL:
    def __init__(self):
        self._client = MongoClient(SECRET_URI)
        self._db = self._client["factoryDB"]
        self._collection = self._db["shifts"]

    def get_shifts(self):
        stage_lookup_employees = {
            "$lookup":{
                "from": "employees",
                "localField": "employees",
                "foreignField": "_id", 
                "as": "employees",
            }
            
        }
        pipeline = [stage_lookup_employees]
        results =list(self._collection.aggregate(pipeline)) 
        return results
        

    def get_shift_by_id(self, id):
        shift = self._collection.find_one({"_id": ObjectId(id)})
        return shift
    
    def add_shift(self, new_shift):
        self._collection.insert_one(new_shift)
        return "Shift Added !"

    def update_shift(self, id, shift_obj):
        self._collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": shift_obj})
        return "Shift Updated !"
  