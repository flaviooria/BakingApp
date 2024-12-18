from features.auth.domain.repositories.auth_repository import AuthRepository


class LoginUseCase:

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def execute(self, email: str, password: str):
        return self.repository.sign_in(email, password)
