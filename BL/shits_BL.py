from DAL.shits_DAL import ShiftsDAL
from bson import ObjectId

class ShiftsBL:
    def __init__(self):
        self._shifts_dal = ShiftsDAL()

    def get_shifts(self):
        shifts = self._shifts_dal.get_shifts()
        return shifts

    def get_shift_by_id(self, id):
        shift = self._shifts_dal.get_shift_by_id(id)
        return shift
    
    def add_shift(self, new_shift):
        resp = self._shifts_dal.add_shift(new_shift)
        return resp

    def update_shift(self, id, shift_obj):
        resp = self._shifts_dal.update_shift(id, shift_obj)
        return resp

    def add_employee_to_shift(self, id, employeeId):
        shift = self._shifts_dal.get_shift_by_id(id)
        shift["employees"].append(ObjectId(employeeId))
        self.update_shift(id,shift)
        return "Employee Added"
