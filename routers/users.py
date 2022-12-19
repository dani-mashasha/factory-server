import functools
from flask import Blueprint, jsonify, request, make_response
from BL.users_BL import UsersBL
from BL.auth_BL import AuthBL



users = Blueprint("users", __name__, url_prefix = "/users")

users_bl = UsersBL()
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
    

@users.route('/', methods=["GET"])
@login_required
def get_users():
    users = users_bl.get_users()
    return jsonify(users)