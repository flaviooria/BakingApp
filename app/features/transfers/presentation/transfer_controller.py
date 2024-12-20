from flask import Blueprint, request, jsonify

from common.middleware.auth_middleware import AuthMiddleware
from entities.entities import User
from features.transfers.data.database.transfer_database import TransferDatabaseImpl
from features.transfers.data.repositories.transfer_repository_impl import TransferRepositoryImpl
from features.transfers.domain.usecases.get_fee_usecase import GetFeeUseCase
from features.transfers.domain.usecases.get_rate_usecase import GetRateUseCase
from features.transfers.domain.usecases.simulate_transfer_usecase import SimulateTransferUseCase
from shared.handle_api_error import handle_msg_error

transfer_router = Blueprint('transfer', __name__, url_prefix="/transfer")

transfer_database_impl = TransferDatabaseImpl()
transfer_repository = TransferRepositoryImpl(transfer_database_impl)
simulate_transfer_use_case = SimulateTransferUseCase(transfer_repository)
get_fee_use_case = GetFeeUseCase(transfer_repository)
get_rate_use_case = GetRateUseCase(transfer_repository)


@transfer_router.post("/simulate", endpoint="simulate_transfer")
@AuthMiddleware.auth_required
def simulate_transfer(_: User):
    try:
        transfer_data = request.get_json()

        result = simulate_transfer_use_case.execute(transfer_data)

        return result.fold(handle_msg_error,
                           lambda amount: (jsonify({"msg": "Amount in target currency: {:.2f}".format(amount)}), 200))
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500


@transfer_router.get("/fees", endpoint="get_fee")
@AuthMiddleware.auth_required
def get_fee(_: User):
    try:
        currency_from = request.args.get("source_currency")
        currency_to = request.args.get("target_currency")

        result = get_fee_use_case.execute(currency_from, currency_to)

        return result.fold(handle_msg_error,
                           lambda fee: (jsonify({"fee": fee}), 200))
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500


@transfer_router.get("/rates", endpoint="get_rate")
@AuthMiddleware.auth_required
def get_rate(_: User):
    try:
        currency_from = request.args.get("source_currency")
        currency_to = request.args.get("target_currency")

        result = get_rate_use_case.execute(currency_from, currency_to)

        return result.fold(handle_msg_error,
                           lambda rate: (jsonify({"rate": rate}), 200))
    except Exception as ex:
        return jsonify({"msg": str(ex)}), 500
