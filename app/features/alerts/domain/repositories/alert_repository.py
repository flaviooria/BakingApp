from abc import ABC, abstractmethod

from common.functions import Either
from exceptions import ApiException


class AlertRepository(ABC):
    @abstractmethod
    def create_alert(self, new_alert: dict) -> Either[ApiException, dict]:
        pass

    @abstractmethod
    def create_alert_balance_drop(self, balance_drop: dict) -> Either[ApiException, dict]:
        pass

    @abstractmethod
    def get_alerts(self, user_id: int) -> Either[ApiException, list[dict]]:
        pass

    @abstractmethod
    def delete_alert(self, alert_id: int) -> Either[ApiException, None]:
        pass
