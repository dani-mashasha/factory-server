import functools
from flask import Blueprint, jsonify, request, make_response
from BL.employees_BL import EmployeesBL
from BL.auth_BL import AuthBL



employees = Blueprint("employees", __name__, url_prefix = "/employees")

employees_bl = EmployeesBL()
auth_bl = AuthBL()


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if request.headers and request.headers.get('x-access-token'):
            token = request.headers.get('x-access-token')
            is_token = auth_bl.verify_token(token)
            if not is_token:
                return make_response({"error" : "Not authorized"},401)
            return func(*args, **kwargs)
        else:
            return make_response({"error" : "No token provided"},401)
    return secure_function
    

@employees.route('/', methods=["GET"])
@login_required
def get_employeess():
    employees = employees_bl.get_employees()
    return jsonify(employees)

@employees.route('/<id>', methods=["GET"])
@login_required
def get_employee_by_id(id):
    employee = employees_bl.get_employee_by_id(id)
    return jsonify(employee)

@employees.route('/', methods=["POST"])
@login_required
def add_employee():
    new_employee = request.json
    resp = employees_bl.add_employee(new_employee)
    return jsonify(resp)

@employees.route('/<id>', methods=["PUT"])
@login_required
def update_employee(id):
    employee_obj = request.json
    resp = employees_bl.update_employee(id,employee_obj)
    return resp

@employees.route('/<id>', methods=["DELETE"])
@login_required
def delete_employee(id):
    resp = employees_bl.delete_employee(id)
    return resp

@employees.route('/<id>/<departmentId>', methods=["PUT"])
@login_required
def add_employee_to_department(id, departmentId):
    print(id,departmentId)
    resp = employees_bl.add_employee_to_department(id, departmentId)
    return resp
