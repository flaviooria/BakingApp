from abc import ABC, abstractmethod

from common.functions import Either
from exceptions import ApiException
from models import User


class UserInterface(ABC):

    @abstractmethod
    def sign_up(self, name: str, email: str, password: str) -> Either[ApiException, User]:
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str) -> Either[ApiException, str]:
        pass
