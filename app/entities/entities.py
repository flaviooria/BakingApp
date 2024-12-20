from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from common.config.database import AbstractBase, Base


class User(Base, AbstractBase):
    __tablename__ = "users"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))

    recurring_expenses = relationship("RecurringExpenses", back_populates="user")

    def __init__(self, *, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User {self.name}"


class RecurringExpenses(Base, AbstractBase):
    __tablename__ = "recurring_expenses"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expense_name = Column(String(255))
    amount = Column(Float)
    frequency = Column(String(50))
    start_date = Column(Date)
    created_at = Column(Date, nullable=True)

    user = relationship("User", back_populates="recurring_expenses")

    def __init__(self, **kw):
        self.user_id = kw["user_id"]
        self.expense_name = kw["expense_name"]
        self.amount = kw["amount"]
        self.start_date = kw["start_date"]
        self.frequency = kw["frequency"]

        super().__init__(**kw)
