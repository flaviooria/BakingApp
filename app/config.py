import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    @classmethod
    def get_uri_db(cls):
        return os.getenv("SQLALCHEMY_DATABASE_URI")

    @classmethod
    def secret_key(cls):
        return os.getenv("SECRET_KEY")
