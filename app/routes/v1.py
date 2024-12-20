from flask import Blueprint

from features.auth.presentation.controller.auth_controller import auth_router
from features.recurring_expenses.presentation.controller.recurring_expenses_controller import recurring_expenses_router
from features.transfers.presentation.transfer_controller import transfer_router

api_v1 = Blueprint("api", __name__, url_prefix="/api")

api_v1.register_blueprint(auth_router)
api_v1.register_blueprint(recurring_expenses_router)
api_v1.register_blueprint(transfer_router)
