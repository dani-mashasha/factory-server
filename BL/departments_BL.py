from DAL.departments_DAL import DepartmentsDAL
from DAL.employees_DAL import EmployeesDAL
from bson import ObjectId

class DepartmentsBL:
    def __init__(self):
        self._departments_dal = DepartmentsDAL()
        self._employees_dal = EmployeesDAL()

    def get_departments(self):
        departments = self._departments_dal.get_departments()
        return departments

    def get_department_by_id(self, id):
        departments = self._departments_dal.get_departments()
        department = list(filter(lambda dep: dep["_id"] == ObjectId(id) ,departments))[0]
        return department

    def add_department(self, new_department):
        new_department["manager"] = ObjectId(new_department["manager"] )
        resp = self._departments_dal.add_department(new_department)
        return resp

    def update_department(self, id, department_obj):
        if "manager" in department_obj:
            department_obj["manager"] = ObjectId(department_obj["manager"] )
        resp = self._departments_dal.update_department(id, department_obj)
        return resp
    
    def delete_department(self, id):
        self._employees_dal.delete_employees_by_departmentId(id)
        resp = self._departments_dal.delete_department(id)
        return resp


