from abc import ABC, abstractmethod

from app.common.functions import Either, Left
from app.exceptions import ApiException
from common.functions import Right
from utils.utils import simulate_transfer_currency, get_fee_from_currencies, Currency, get_rate_from_currencies


class TransferDatabase(ABC):
    @abstractmethod
    def simulate_transfer(self, transfer_data: dict) -> Either[ApiException, float]:
        pass

    @abstractmethod
    def get_fee(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        pass

    @abstractmethod
    def get_rate(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        pass


class TransferDatabaseImpl(TransferDatabase):

    def simulate_transfer(self, transfer_data: dict) -> Either[ApiException, float]:
        try:
            if transfer_data is None or transfer_data == {}:
                raise ApiException("No empty fields allowed.", 400)

            for _, value in transfer_data.items():
                if value is None or value == "":
                    raise ApiException("No empty fields allowed.", 400)

            currency_from = transfer_data["target_currency"]
            currency_to = transfer_data["source_currency"]
            amount = transfer_data["amount"]

            total_amount = simulate_transfer_currency(currency_from, currency_to, amount)

            return Right(total_amount)
        except ApiException as apex:
            return Left(apex)
        except Exception as ex:
            return Left(ApiException(str(ex), 404))

    def get_fee(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        try:
            if currency_from is None or currency_from == "" or currency_to is None or currency_to == "":
                raise ApiException("No empty fields allowed.", 400)

            fee = get_fee_from_currencies(currency_from, currency_to)

            return Right(fee)

        except ApiException as apex:
            return Left(apex)
        except Exception as ex:
            return Left(ApiException(str(ex), 404))

    def get_rate(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        try:
            if currency_from is None or currency_from == "" or currency_to is None or currency_to == "":
                raise ApiException("No empty fields allowed.", 400)

            rate = get_rate_from_currencies(currency_from, currency_to)

            return Right(rate)
        except ApiException as apex:
            return Left(apex)
        except Exception as ex:
            return Left(ApiException(str(ex), 404))
