from bcrypt import hashpw, checkpw, gensalt


class CryptPassword:

    @staticmethod
    def encrypt_password(password_plain: str):
        return hashpw(password_plain.encode("utf-8"), gensalt(10)).decode("utf-8")

    @staticmethod
    def decrypt_password(password_plain, password_hash):
        return checkpw(password_plain.encode("utf-8"), password_hash.encode("utf-8"))
