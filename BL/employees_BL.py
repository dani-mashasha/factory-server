from DAL.employees_DAL import EmployeesDAL
from DAL.shits_DAL import ShiftsDAL
from bson import ObjectId
import datetime


class EmployeesBL:
    def __init__(self):
        self._employees_dal = EmployeesDAL()
        self._shifts_dal = ShiftsDAL()
    
    def get_employees(self):
        employees = self._employees_dal.get_employees()
        return employees

    def get_employee_by_id(self, id):
        employees = self._employees_dal.get_employees()
        employee = list(filter(lambda emp : emp["_id"] == ObjectId(id),employees))[0]
        return employee

    def add_employee(self, new_employee):
        new_employee["departmentId"] = ObjectId(new_employee["departmentId"])
        new_employee["startWorkYear"] = datetime.date.today().year
        resp = self._employees_dal.add_employee(new_employee)
        return resp

    def update_employee(self, id, employee_obj):
        if "departmentId" in employee_obj:
            employee_obj["departmentId"] = ObjectId(employee_obj["departmentId"])
        resp = self._employees_dal.update_employee(id,employee_obj)
        return resp
    
    def delete_employee(self, id):
        shifts = self._shifts_dal.get_shifts()
        for shift in shifts:
            emp_list = []
            for employee in shift["employees"]:
                if employee["_id"] != ObjectId(id):
                    emp_list.append(employee["_id"])
            if len(emp_list) != len(shift["employees"]):
                self._shifts_dal.update_shift(shift["_id"], {"employees": emp_list})

        resp = self._employees_dal.delete_employee(id)
        return resp


    def add_employee_to_department(self, id, departmentId):
        employee = self._employees_dal.get_employee_by_id(id)
        employee["departmentId"]= ObjectId(departmentId)
        self.update_employee(id,employee)
        return "Employee Added"