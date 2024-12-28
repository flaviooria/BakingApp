from abc import ABC, abstractmethod

import pandas as pd
from sqlalchemy import select

from common.config.database import db_session
from common.functions import Either, Left, Right
from entities.entities import Alerts
from exceptions import ApiException


class AlertsDatabase(ABC):

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


def verify_data_keys(data: dict, keys: list[str]) -> None:
    for key in keys:
        if data[key] == "" or data[key] is None:
            raise ApiException("No empty fields allowed.", 400)


class AlertsImpl(AlertsDatabase):

    def get_alerts(self, user_id: int) -> Either[ApiException, list[dict]]:
        try:
            if user_id is None or user_id == "" or user_id == 0:
                raise ApiException("No user id provided.", 400)

            alerts = db_session.execute(select(Alerts).where(Alerts.user_id == user_id)).scalars().all()

            alerts_list = [alert.to_dict() for alert in alerts]

            alerts_df = pd.DataFrame(alerts_list)
            alerts_df.drop(columns=["created_at"], inplace=True, axis=1)

            return Right(alerts_df.to_dict(orient="records"))

        except ApiException as apex:
            return Left(apex)

    def delete_alert(self, alert_id: int) -> Either[ApiException, None]:
        try:
            if alert_id is None:
                raise ApiException("Missing alert ID.", 400)

            if alert_id == "" or alert_id == 0:
                raise ApiException("No empty fields allowed.", 400)

            alert_to_delete = db_session.execute(select(Alerts).where(Alerts.id == alert_id)).scalar()

            if alert_to_delete is None:
                raise ApiException("Alert not found.", 404)

            db_session.delete(alert_to_delete)
            db_session.commit()

            return Right(None)

        except ApiException as apex:
            return Left(apex)

    def create_alert_balance_drop(self, balance_drop: dict) -> Either[ApiException, dict]:
        try:
            if balance_drop is None or balance_drop == {}:
                raise ApiException("No data provided.", 400)

            keys = ["balance_drop_threshold", "user_id"]

            verify_data_keys(balance_drop, keys)

            alert_to_save = Alerts(**balance_drop)

            db_session.add(alert_to_save)
            db_session.commit()

            alert_dict = alert_to_save.to_dict()
            del alert_dict["created_at"]
            del alert_dict["target_amount"]
            del alert_dict["alert_threshold"]

            return Right(alert_dict)
        except ApiException as apex:
            return Left(apex)

    def create_alert(self, new_alert: dict) -> Either[ApiException, dict]:

        try:
            if new_alert is None or new_alert == {}:
                raise ApiException("No data provided.", 400)

            keys = ["target_amount", "alert_threshold", "user_id"]

            verify_data_keys(new_alert, keys)

            alert_to_save = Alerts(**new_alert)

            db_session.add(alert_to_save)
            db_session.commit()

            alert_dict = alert_to_save.to_dict()
            del alert_dict["created_at"]
            del alert_dict["balance_drop_threshold"]

            return Right(alert_dict)

        except ApiException as apex:
            return Left(apex)
