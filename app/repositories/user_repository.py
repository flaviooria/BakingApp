from app.interfaces.user_interface import UserInterface
from datasources.user_database import UserDatabaseInterface


class UserRepositoryImpl(UserInterface):

    def __init__(self, user_database: UserDatabaseInterface):
        self.user_database = user_database

    def sign_up(self, name: str, email: str, password: str):
        return self.user_database.sign_up(name, email, password)

    def sign_in(self, email: str, password: str):
        return self.user_database.sign_in(email, password)
