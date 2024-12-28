from features.alerts.domain.repositories.alert_repository import AlertRepository


class GetAlertsUseCase:
    def __init__(self, alerts_repository: AlertRepository):
        self.alerts_repository = alerts_repository

    def execute(self, user_id: int):
        return self.alerts_repository.get_alerts(user_id)
