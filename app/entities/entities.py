import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, DateTime
from sqlalchemy.orm import relationship
from typing_extensions import overload

from common.config.database import AbstractBase, Base


class User(Base, AbstractBase):
    __tablename__ = "users"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))

    recurring_expenses = relationship("RecurringExpenses", back_populates="user")
    alerts = relationship("Alerts", back_populates="user")

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


class Alerts(Base, AbstractBase):
    __tablename__ = "alerts"

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_amount = Column(Float)
    alert_threshold = Column(Float)
    balance_drop_threshold = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.now())

    user = relationship("User", back_populates="alerts")

    @overload
    def __init__(self, user_id: int, balance_drop_threshold: float):
        pass

    @overload
    def __init__(self, user_id: int, target_amount: float, alert_threshold: float):
        pass

    def __init__(self, **kw):
        self.user_id = kw["user_id"]
        self.target_amount = kw.get("target_amount", 0)
        self.alert_threshold = kw.get("alert_threshold", 0)
        self.balance_drop_threshold = kw.get("balance_drop_threshold", 0)

        super().__init__(**kw)
