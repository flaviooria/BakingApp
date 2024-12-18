from typing import ClassVar

from jwt import encode as JwtEncode, decode as JwtDecode

from common.config.settings import Settings


class JwtUtil:
    _secret: ClassVar[str] = Settings.secret_key()

    @staticmethod
    def encode(payload: dict):
        print(payload)
        return JwtEncode(payload, JwtUtil._secret, algorithm="HS256")

    @staticmethod
    def decode(jwt: str) -> dict:
        decoded = JwtDecode(jwt, JwtUtil._secret, algorithms=["HS256"])

        return decoded
