from common.functions import Either
from exceptions import ApiException
from features.transfers.data.database.transfer_database import TransferDatabase
from features.transfers.domain.repositories.transfer_repository import TransferRepository
from utils.utils import Currency


class TransferRepositoryImpl(TransferRepository):

    def __init__(self, transfer_database: TransferDatabase):
        self.transfer_database = transfer_database

    def simulate_transfer(self, transfer_data: dict) -> Either[ApiException, float]:
        return self.transfer_database.simulate_transfer(transfer_data)

    def get_fee(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        return self.transfer_database.get_fee(currency_from, currency_to)

    def get_rate(self, currency_from: Currency, currency_to: Currency) -> Either[ApiException, float]:
        return self.transfer_database.get_rate(currency_from, currency_to)
