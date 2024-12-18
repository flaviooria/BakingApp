from features.auth.domain.repositories.auth_repository import AuthRepository


class RegisterUseCase:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def execute(self, name: str, email: str, password: str):
        return self.repository.sign_up(name, email, password)
