from abc import ABC, abstractmethod

import pandas as pd
from sqlalchemy import select

from common.config.database import db_session
from common.functions import Either, Left, Right
from entities.entities import RecurringExpenses
from exceptions import ApiException


class RecurringExpensesDatabase(ABC):

    @abstractmethod
    def create(self, new_expense: dict) -> Either[ApiException, dict]:
        pass

    @abstractmethod
    def get_recurring_expenses(self, user_id: int) -> Either[ApiException, list[dict]]:
        pass

    @abstractmethod
    def update_expense(self, expense_id: int, new_expense: dict) -> Either[ApiException, dict]:
        pass

    @abstractmethod
    def delete_expense(self, expense_id: int) -> Either[ApiException, None]:
        pass

    @abstractmethod
    def get_expenses_projection(self, user_id: int) -> Either[ApiException, list[dict]]:
        pass


def mapper_expenses(expenses: list[RecurringExpenses]):
    return [expense.to_dict() for expense in expenses]


class RecurringExpensesImpl(RecurringExpensesDatabase):
    def get_recurring_expenses(self, user_id: int) -> Either[ApiException, list[dict]]:
        try:
            recurring_expenses = db_session.query(RecurringExpenses).where(RecurringExpenses.user_id == user_id).all()

            expenses_list = mapper_expenses(recurring_expenses)
            expenses_df = pd.DataFrame(expenses_list)
            expenses_df["start_date"] = expenses_df["start_date"].apply(lambda date: date.strftime("%Y-%m-%d"))

            return Right(expenses_df.to_dict(orient="records"))
        except ApiException as apex:
            return Left(apex)

    def create(self, new_expense: dict) -> Either[ApiException, dict]:
        try:
            if new_expense is None:
                raise ApiException("No data provided.", 400)

            keys = ["expense_name", "amount", "frequency", "star_date"]
            for key in new_expense.keys():
                if key in keys and new_expense[key] == "" or new_expense[key] is None:
                    raise ApiException("No empty fields allowed.", 400)

            recurring_exp = RecurringExpenses(**new_expense)

            db_session.add(recurring_exp)
            db_session.commit()

            expense_df = pd.DataFrame([recurring_exp.to_dict()])
            expense_df["start_date"] = expense_df["start_date"].apply(lambda date: date.strftime("%Y-%m-%d"))

            return Right(expense_df.to_dict(orient="records")[0])
        except ApiException as apex:
            return Left(apex)

    def update_expense(self, expense_id: int, new_expense: dict) -> Either[ApiException, dict]:
        try:
            if new_expense is None or new_expense == {}:
                raise ApiException("No data provided.", 400)

            keys = ["expense_name", "amount", "frequency", "star_date"]
            for key in new_expense.keys():
                if key in keys and new_expense[key] == "" or new_expense[key] is None:
                    raise ApiException("No empty fields allowed.", 400)

            recurring_exp = db_session.execute(
                select(RecurringExpenses).where(RecurringExpenses.id == expense_id)).scalar_one_or_none()

            if recurring_exp is None:
                raise ApiException("Expense not found.", 404)

            for key in new_expense.keys():
                setattr(recurring_exp, key, new_expense[key])

            db_session.commit()

            expense_df = pd.DataFrame([recurring_exp.to_dict()])
            expense_df["start_date"] = expense_df["start_date"].apply(lambda date: date.strftime("%Y-%m-%d"))

            return Right(expense_df.to_dict(orient="records")[0])


        except ApiException as apex:
            return Left(apex)

    def delete_expense(self, expense_id: int) -> Either[ApiException, None]:
        try:
            recurring_exp = db_session.execute(
                select(RecurringExpenses).where(RecurringExpenses.id == expense_id)).scalar_one_or_none()

            if recurring_exp is None:
                raise ApiException("Expense not found.", 404)

            db_session.delete(recurring_exp)
            db_session.commit()

            return Right(None)

        except ApiException as apex:
            return Left(apex)

    def get_expenses_projection(self, user_id: int) -> Either[ApiException, list[dict]]:
        try:
            expenses = db_session.query(RecurringExpenses).where(RecurringExpenses.user_id == user_id).all()
            expenses_mapper = [expense.to_dict() for expense in expenses]

            expenses_df = pd.DataFrame(expenses_mapper)

            if expenses_df.empty:
                return Right([])

            expenses_df["start_date"] = pd.to_datetime(expenses_df["start_date"])
            expenses_df["month"] = expenses_df["start_date"].dt.to_period("M")

            monthly_expenses: pd.DataFrame = (expenses_df.groupby("month")["amount"].sum().reset_index())

            # Obtengo el promedio de gastos por mes y el último mes registrado
            avg_amount_per_month = monthly_expenses["amount"].mean()
            last_month = monthly_expenses["month"].max()
            # Genero la proyección de los próximos 12 meses
            projection_future_months = pd.period_range(start=last_month + 1, periods=12, freq="M")

            projection_df = pd.DataFrame({"month": projection_future_months, "amount": avg_amount_per_month})
            # Concat para unir los dataframes y que tanto los meses calculados como los reales estén en un solo dataframe
            projection_calculated_df = pd.concat([monthly_expenses, projection_df])
            projection_calculated_df.sort_values(by="month", inplace=True)
            projection_calculated_df["month"] = projection_calculated_df["month"].dt.strftime("%Y-%m")
            projection_calculated_df.rename(columns={"amount": "recurring_expenses"}, inplace=True)

            return Right(projection_calculated_df.to_dict(orient="records"))

        except ApiException as apex:
            return Left(apex)
