from pymongo import MongoClient
from bson import ObjectId
# from test import mongourl
from dotenv import load_dotenv
load_dotenv()
import os

SECRET_URI = os.getenv("MONGOURI")


class EmployeesDAL:
    def __init__(self):
        self._client = MongoClient(SECRET_URI)
        self._db = self._client["factoryDB"]
        self._collection = self._db["employees"]
    
    def get_employees(self):
        stage_lookup_department = {
            "$lookup": {
                "from": "departments", 
                "localField": "departmentId", 
                "foreignField": "_id", 
                "as": "department",
            },
        }
        stage_lookup_shifts = {
            "$lookup":{
                "from": "shifts",
                "localField": "_id",
                "foreignField": "employees", 
                "as": "shifts",
            }
            
        }
        unwind = { "$unwind": "$department" }
        pipeline = [stage_lookup_department, stage_lookup_shifts,unwind]
        results =list(self._collection.aggregate(pipeline)) 
        return results

    def get_employee_by_id(self, id):
        employee = self._collection.find_one({"_id": ObjectId(id)})
        return employee
       
    def add_employee(self, new_employee):
        self._collection.insert_one(new_employee)
        return "Employee Added !"

    def update_employee(self, id, employee_obj):
        self._collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": employee_obj})
        return "Employee Updated !"
    
    def delete_employee(self, id):
        self._collection.find_one_and_delete({"_id": ObjectId(id)})
        return "Employee Deleted !"

    def delete_employees_by_departmentId(self, departmentId):
        self._collection.delete_many({"departmentId": ObjectId(departmentId)})
        return "Employees Deleted !"
