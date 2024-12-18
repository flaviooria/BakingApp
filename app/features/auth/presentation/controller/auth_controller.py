from flask import Blueprint, request, jsonify

from exceptions import ApiException
from features.auth.data.database.auth_database import AuthDatabaseImpl
from features.auth.data.repositories.auth_repository_impl import AuthRepositoryImpl
from features.auth.domain.usecases.login_usecase import LoginUseCase
from features.auth.domain.usecases.register_usecase import RegisterUseCase
from shared.handle_api_error import handle_error

auth_router = Blueprint("auth_router", __name__, url_prefix="/auth")

auth_db_impl = AuthDatabaseImpl()
auth_repository = AuthRepositoryImpl(auth_db_impl)
login_use_case = LoginUseCase(auth_repository)
register_use_case = RegisterUseCase(auth_repository)


@auth_router.post("/register")
def register():
    try:
        body = request.get_json()

        if "name" not in body or "email" not in body or "password" not in body:
            raise ApiException("All fields are required.", 400)

        result = register_use_case.execute(**body)

        return result.fold(handle_error, lambda user: (
            jsonify({"name": user.name, "email": user.email, "hashedPassword": user.password}), 201))
    except Exception as ex:
        return jsonify(str(ex)), 500


@auth_router.post("/login")
def login():
    try:
        body = request.get_json()

        if "email" not in body or "password" not in body:
            raise ApiException("Bad credentials", 400)

        result = login_use_case.execute(**body)

        return result.fold(handle_error, lambda token: (jsonify({"token": token}), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500
