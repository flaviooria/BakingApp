from flask import request, Blueprint, jsonify

from common.middleware.auth_middleware import AuthMiddleware
from entities.entities import User
from features.alerts.data.database.alerts_database import AlertsImpl
from features.alerts.data.repositories.alerts_repository_impl import AlertsRepositoryImpl
from features.alerts.domain.usecases.create_alert_usecase import CreateAlertUseCase
from features.alerts.domain.usecases.create_balance_drop_usecase import CreateBalanceDropUseCase
from features.alerts.domain.usecases.delete_alert_usecase import DeleteAlertUseCase
from features.alerts.domain.usecases.get_alerts_usecase import GetAlertsUseCase
from shared.handle_api_error import handle_msg_error

alerts_router = Blueprint('alerts', __name__, url_prefix="/alerts")

alert_db_impl = AlertsImpl()
alert_repository = AlertsRepositoryImpl(alert_db_impl)
create_alert_use_case = CreateAlertUseCase(alert_repository)
create_balance_drop_use_case = CreateBalanceDropUseCase(alert_repository)
get_alerts_use_case = GetAlertsUseCase(alert_repository)
delete_alert_use_case = DeleteAlertUseCase(alert_repository)


@alerts_router.post("/amount_reached", endpoint="amount_reached")
@AuthMiddleware.auth_required
def amount_reached(user: User):
    try:
        body = request.get_json()

        body.update({"user_id": user.id})

        result = create_alert_use_case.execute(body)

        return result.fold(handle_msg_error, lambda alert: (
            jsonify({"msg": "Correctly added savings alert!", "data": alert}), 201))

    except Exception as ex:
        return jsonify(str(ex)), 500


@alerts_router.post("/balance_drop", endpoint="balance_drop")
@AuthMiddleware.auth_required
def balance_drop(user: User):
    try:
        body = request.get_json()

        body.update({"user_id": user.id})

        result = create_balance_drop_use_case.execute(body)

        return result.fold(handle_msg_error, lambda alert: (
            jsonify({"msg": "Correctly added balance drop alert!", "data": alert}), 201))

    except Exception as ex:
        return jsonify(str(ex)), 500


@alerts_router.get("/list", endpoint="get_alerts")
@AuthMiddleware.auth_required
def get_alerts(user: User):
    try:
        results = get_alerts_use_case.execute(user.id)

        return results.fold(handle_msg_error, lambda alerts: (jsonify({"data": alerts}), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500


@alerts_router.delete("/delete", endpoint="delete_alert")
@AuthMiddleware.auth_required
def delete_alert(_):
    try:
        body = request.get_json()

        result = delete_alert_use_case.execute(body.get("alert_id", None))

        return result.fold(handle_msg_error, lambda _: (jsonify({"msg": "Alert deleted successfully."}), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500
