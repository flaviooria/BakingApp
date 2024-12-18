from common.functions import Either
from entities.entities import User
from exceptions import ApiException
from features.auth.data.database.auth_database import AuthDatabase
from features.auth.domain.repositories.auth_repository import AuthRepository

class AuthRepositoryImpl(AuthRepository):

    def __init__(self, auth_db: AuthDatabase):
        self._auth_db = auth_db

    def sign_up(self, name: str, email: str, password: str) -> Either[ApiException, User]:
        return self._auth_db.sign_up(name, email, password)

    def sign_in(self, email: str, password: str) -> Either[ApiException, str]:
        return self._auth_db.sign_in(email, password)
