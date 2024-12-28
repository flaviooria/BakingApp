from common.functions import Either
from exceptions import ApiException
from features.alerts.data.database.alerts_database import AlertsDatabase
from features.alerts.domain.repositories.alert_repository import AlertRepository


class AlertsRepositoryImpl(AlertRepository):
    def __init__(self, alert_database: AlertsDatabase):
        self.alert_database = alert_database

    def create_alert(self, new_alert: dict) -> Either[ApiException, dict]:
        return self.alert_database.create_alert(new_alert)

    def create_alert_balance_drop(self, balance_drop: dict) -> Either[ApiException, dict]:
        return self.alert_database.create_alert_balance_drop(balance_drop)

    def get_alerts(self, user_id: int) -> Either[ApiException, list[dict]]:
        return self.alert_database.get_alerts(user_id)

    def delete_alert(self, alert_id: int) -> Either[ApiException, None]:
        return self.alert_database.delete_alert(alert_id)
