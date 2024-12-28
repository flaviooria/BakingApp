from features.alerts.domain.repositories.alert_repository import AlertRepository


class DeleteAlertUseCase:
    def __init__(self, alerts_repository: AlertRepository):
        self.alerts_repository = alerts_repository

    def execute(self, alert_id: int):
        return self.alerts_repository.delete_alert(alert_id)
