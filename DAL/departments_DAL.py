from cgitb import lookup
from pymongo import MongoClient
from bson import ObjectId
# from test import mongourl
from dotenv import load_dotenv
load_dotenv()
import os

SECRET_URI = os.getenv("MONGOURI")

class DepartmentsDAL:
    def __init__(self):
        self._client = MongoClient(SECRET_URI)
        self._db = self._client["factoryDB"]
        self._collection = self._db["departments"]
   
    def get_departments(self):
        stage_lookup_employees = {
            "$lookup": {
                "from": "employees", 
                "localField": "_id", 
                "foreignField": "departmentId", 
                "as": "employees",
            },
        }
        stage_lookup_manager = {
            "$lookup":{
                "from": "employees",
                "localField": "manager",
                "foreignField": "_id", 
                "as": "manager",
            }
            
        }
        unwind = { "$unwind": "$manager" }
        pipeline = [stage_lookup_employees, stage_lookup_manager,unwind]
        results =list(self._collection.aggregate(pipeline)) 
        return results
    
    def add_department(self, new_department):
        self._collection.insert_one(new_department)
        return "Department Added !"

    def update_department(self, id, department_obj):
        self._collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": department_obj})
        return "Department Updated !"
    
    def delete_department(self, id):
        self._collection.find_one_and_delete({"_id": ObjectId(id)})
        return "Department Deleted !"


