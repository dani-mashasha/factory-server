import functools
from flask import Blueprint, jsonify, request, make_response
from BL.shits_BL import ShiftsBL
from BL.auth_BL import AuthBL



shifts = Blueprint("shifts", __name__,url_prefix = "/shifts")

shifts_bl = ShiftsBL()
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
    

@shifts.route('/', methods=["GET"])
@login_required
def get_shifts():
    shifts = shifts_bl.get_shifts()
    return jsonify(shifts)

@shifts.route('/<id>', methods=["GET"])
@login_required
def get_shift_by_id(id):
    shift = shifts_bl.get_shift_by_id(id)
    return jsonify(shift)

@shifts.route('/', methods=["POST"])
@login_required
def add_shift():
    new_shift = request.json
    resp = shifts_bl.add_shift(new_shift)
    return jsonify(resp)

@shifts.route('/<id>', methods=["PUT"])
@login_required
def update_shift(id):
    shift_obj = request.json
    resp = shifts_bl.update_shift(id, shift_obj)
    return resp

@shifts.route('/<id>/<employeeId>', methods=["PUT"])
@login_required
def add_employee_to_shift(id, employeeId):
    resp = shifts_bl.add_employee_to_shift(id, employeeId)
    return resp
