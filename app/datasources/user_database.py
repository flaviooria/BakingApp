from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta

from sqlalchemy import select

from common.functions import Either, Left, Right
from database import db_session
from exceptions import ApiException
from models import User
from utils.jwt_util import JwtUtil
from utils.passwords_utils import CryptPassword
from utils.utils import validate_email


class UserDatabaseInterface(ABC):

    @abstractmethod
    def sign_up(self, name: str, email: str, password: str) -> Either[ApiException, User]:
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str) -> Either[ApiException, str]:
        pass


class UserDatabaseImpl(UserDatabaseInterface):
    def sign_in(self, email: str, password: str) -> Either[ApiException, str]:
        try:
            if (email == "" or email is None) or (password == "" or password is None):
                raise ApiException("Bad credentials.", 401)

            user_exist = db_session.execute(select(User).where(User.email == email)).scalar_one_or_none()

            if user_exist is None:
                raise ApiException(f"User not found for the given email: {email}", 400)

            if not CryptPassword.decrypt_password(password, user_exist.password):
                raise ApiException("Bad credentials.", 401)

            print(user_exist.email)

            expires_token = datetime.now(timezone.utc) + timedelta(hours=1)
            token = JwtUtil.encode({"sub": user_exist.email, "exp": expires_token})

            return Right(token)
        except ApiException as apex:
            return Left(apex)
        except Exception as ex:
            return Left(ApiException(str(ex), 500))

    def sign_up(self, name: str, email: str, password: str):
        try:
            if (name == "" or name is None) or (email == "" or email is None) or (password == "" or password is None):
                raise ApiException("No empty fields allowed.", 400)

            if not validate_email(email):
                raise ApiException(f"Invalid email: {email}", 400)

            user_exist = db_session.execute(select(User).where(User.email == email)).first()

            if user_exist is not None:
                raise ApiException("Email already exists.", 400)

            user_to_store = User(name=name, email=email)
            user_to_store.password = CryptPassword.encrypt_password(password)

            db_session.add(user_to_store)
            db_session.commit()

            return Right(user_to_store)

        except ApiException as apex:
            return Left(apex)
