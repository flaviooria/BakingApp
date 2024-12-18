from flask import Blueprint

from features.auth.presentation.controller.auth_controller import auth_router

api_v1 = Blueprint("api", __name__, url_prefix="/api")

api_v1.register_blueprint(auth_router)
