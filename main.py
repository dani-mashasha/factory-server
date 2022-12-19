import os
from flask import Flask
import json
from bson import ObjectId
from flask_cors import CORS
from routers.departments import departments
from routers.employees import employees
from routers.shifts import shifts
from routers.users import users
from routers.auth import auth


class JSONEncoder(json.JSONEncoder):
    def default(self, obj) :
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self,obj)

app = Flask(__name__)
CORS(app,resources={r'/*': {'origins': '*'}},supports_credentials=True)
app.json_encoder = JSONEncoder


app.register_blueprint(departments)
app.register_blueprint(employees)
app.register_blueprint(shifts)
app.register_blueprint(users)
app.register_blueprint(auth)


app.run()
