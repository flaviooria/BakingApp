from features.alerts.domain.repositories.alert_repository import AlertRepository


class CreateBalanceDropUseCase:
    def __init__(self, alert_repository: AlertRepository):
        self.alert_repository = alert_repository

    def execute(self, balance_drop):
        return self.alert_repository.create_alert_balance_drop(balance_drop)
