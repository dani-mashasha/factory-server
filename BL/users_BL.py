from DAL.users_DAL import UsersDAL

class UsersBL:
    def __init__(self):
        self._users_dal = UsersDAL()

    def get_users(self):
        users = self._users_dal.get_users()
        return users
