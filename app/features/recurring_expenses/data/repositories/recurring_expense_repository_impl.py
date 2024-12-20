from common.functions import Either
from exceptions import ApiException
from features.recurring_expenses.data.database.recurring_expense_database import RecurringExpensesDatabase
from features.recurring_expenses.domain.repositories.recurring_expenses_repository import RecurringExpensesRepository


class RecurringExpensesRepositoryImpl(RecurringExpensesRepository):

    def __init__(self, recurring_exp_db: RecurringExpensesDatabase):
        self.recurring_exp_db = recurring_exp_db

    def create(self, new_expense: dict) -> Either[ApiException, dict]:
        return self.recurring_exp_db.create(new_expense)

    def get_recurring_expenses(self, user_id: int) -> Either[ApiException, list[dict]]:
        return self.recurring_exp_db.get_recurring_expenses(user_id)

    def update_expense(self, expense_id: int, new_expense: dict) -> Either[ApiException, dict]:
        return self.recurring_exp_db.update_expense(expense_id, new_expense)

    def delete_expense(self, expense_id: int) -> Either[ApiException, None]:
        return self.recurring_exp_db.delete_expense(expense_id)

    def get_expenses_projection(self, user_id: int) -> Either[ApiException, list[dict]]:
        return self.recurring_exp_db.get_expenses_projection(user_id)
