from flask import Blueprint,jsonify, request, make_response
from BL.auth_BL import AuthBL

auth = Blueprint('auth', __name__, url_prefix = "/auth")

auth_bl = AuthBL()


@auth.route('/login', methods=['POST'])
def login():
    username = request.json["username"]
    email = request.json["email"]

    token = auth_bl.get_token(username,email)
    if token is not None:
        return make_response({"token" : token },200)
    else:
        return make_response({"error" : "You're not authorized" },401)
