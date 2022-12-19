import jwt
from DAL.users_ws_DAL import UsersWSDAL

class AuthBL:
    def __init__(self):
        self.__key = "server_key"
        self.__algorithm = "HS256"
        self._users_ws_dal = UsersWSDAL()

    def get_token(self,username, email):
        user_id = self.__check_user(username,email)
        token = None
        if user_id is not None:
            token = jwt.encode({"userid" : user_id}, self.__key, self.__algorithm)
        return token

    def verify_token(self, token):
        data = jwt.decode(token, self.__key, self.__algorithm)
        user_id = data["userid"]
        users = self._users_ws_dal.get_users()
        user = list(filter(lambda us : us["id"] == user_id ,users))[0]
        if user is not None:
            return True
        return False


    def __check_user(self,username, email):
        users = self._users_ws_dal.get_users()
        user = list(filter(lambda us : us["username"] == username and us["email"] == email ,users))[0]
        return user["id"]

