from abc import abstractmethod, ABC

from common.functions import Either
from exceptions import ApiException
from utils.utils import Currency


class TransferRepository(ABC):
    @abstractmethod
    def simulate_transfer(self, transfer_data: dict) -> Either[ApiException, float]:
        pass

    @abstractmethod
    def get_fee(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        pass

    @abstractmethod
    def get_rate(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        pass
