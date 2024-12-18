from typing import ClassVar

from jwt import encode as JwtEncode, decode as JwtDecode

from config import Config


class JwtUtil:
    _secret: ClassVar[str] = Config.secret_key()

    @staticmethod
    def encode(payload: dict):
        print(payload)
        return JwtEncode(payload, JwtUtil._secret, algorithm="HS256")

    @staticmethod
    def decode(jwt: str) -> dict:
        decoded = JwtDecode(jwt, JwtUtil._secret, algorithms=["HS256"])

        return decoded
