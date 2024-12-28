from features.alerts.domain.repositories.alert_repository import AlertRepository


class CreateAlertUseCase:
    def __init__(self, alert_repository: AlertRepository):
        self.alert_repository = alert_repository

    def execute(self, alert: dict):
        return self.alert_repository.create_alert(alert)
