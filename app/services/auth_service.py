from interfaces.user_interface import UserInterface


class AuthService:

    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    def register(self, name: str, email: str, password: str):
        return self.user_repository.sign_up(name, email, password)

    def login(self, email: str, password: str):
        return self.user_repository.sign_in(email, password)
