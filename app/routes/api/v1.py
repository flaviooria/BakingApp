from flask import Blueprint

from app.routes.api.auth_router import auth_router

api_v1 = Blueprint("api", __name__, url_prefix="/api")

api_v1.register_blueprint(auth_router)
