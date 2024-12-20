from functools import wraps

from flask import request, jsonify
from sqlalchemy import select

from common.config.database import db_session
from entities.entities import User
from utils.jwt_util import JwtUtil


class AuthMiddleware:

    @staticmethod
    def auth_required(function):
        wraps(function)

        def decorator(*args, **kwargs):
            token = None

            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return jsonify({
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }), 401

            try:
                payload = JwtUtil.decode(token)

                user_email = payload["sub"]

                current_user = db_session.execute(select(User).where(User.email == user_email)).scalar_one_or_none()

                if current_user is None:
                    return jsonify({
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized"
                    }), 401

                return function(current_user, *args, **kwargs)

            except Exception as e:
                return jsonify({
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }), 500

        return decorator
