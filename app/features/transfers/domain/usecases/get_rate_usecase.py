from typing import cast

from features.transfers.domain.repositories.transfer_repository import TransferRepository
from utils.utils import Currency


class GetRateUseCase:
    def __init__(self, fee_repository: TransferRepository):
        self.fee_repository = fee_repository

    def execute(self, currency_from: str, currency_to: str):
        return self.fee_repository.get_rate(cast(Currency, currency_from), cast(Currency, currency_to))
