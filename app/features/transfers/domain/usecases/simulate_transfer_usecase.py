from features.transfers.domain.repositories.transfer_repository import TransferRepository


class SimulateTransferUseCase:
    def __init__(self, transfer_repository: TransferRepository):
        self.transfer_repository = transfer_repository

    def execute(self, transfer: dict):
        return self.transfer_repository.simulate_transfer(transfer)