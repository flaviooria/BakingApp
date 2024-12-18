from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))


    def __init__(self, *, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User {self.name}"
