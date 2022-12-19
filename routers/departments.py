from flask import Blueprint, jsonify, request, make_response
from BL.departments_BL import DepartmentsBL
from BL.auth_BL import AuthBL
import functools

departments = Blueprint("departments", __name__, url_prefix = "/departments")

departments_bl = DepartmentsBL()
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
    

@departments.route('/', methods=["GET"])
@login_required
def get_departments():
    departments = departments_bl.get_departments()
    return jsonify(departments)

@departments.route('/<id>', methods=["GET"])
@login_required
def get_department_by_id(id):
    department = departments_bl.get_department_by_id(id)
    return jsonify(department)

@departments.route('/', methods=["POST"])
@login_required
def add_department():
    new_departrment = request.json
    resp = departments_bl.add_department(new_departrment)
    return jsonify(resp)

@departments.route('/<id>', methods=["PUT"])
@login_required
def update_deoartment(id):
    department_obj = request.json
    resp = departments_bl.update_department(id,department_obj)
    return resp

@departments.route('/<id>', methods=["DELETE"])
@login_required
def delete_department(id):
    resp = departments_bl.delete_department(id)
    return resp