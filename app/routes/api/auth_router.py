from flask import Blueprint, request, jsonify

from datasources.user_database import UserDatabaseImpl
from exceptions import ApiException
from repositories.user_repository import UserRepositoryImpl
from services.auth_service import AuthService

auth_router = Blueprint("auth_router", __name__, url_prefix="/auth")

user_db_impl = UserDatabaseImpl()
user_repository = UserRepositoryImpl(user_db_impl)
auth_servie = AuthService(user_repository)


def handle_error(apex: ApiException):
    return jsonify(apex.msg), apex.status_code


@auth_router.post("/register")
def register():
    try:
        body = request.get_json()

        if "name" not in body or "email" not in body or "password" not in body:
            raise ApiException("All fields are required.", 400)

        result = auth_servie.register(**body)

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

        result = auth_servie.login(**body)

        return result.fold(handle_error, lambda token: (jsonify({"token": token}), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500
