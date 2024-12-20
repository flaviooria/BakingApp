from common.functions import Either
from entities.entities import RecurringExpenses
from exceptions import ApiException
from features.recurring_expenses.domain.repositories.recurring_expenses_repository import RecurringExpensesRepository


class UpdateRecurringExpenseUseCase:
    def __init__(self, recurring_exp_repository: RecurringExpensesRepository):
        self.recurring_exp_repository = recurring_exp_repository

    def execute(self, expense_id: int, new_expense: dict) -> Either[ApiException, RecurringExpenses]:
        return self.recurring_exp_repository.update_expense(expense_id, new_expense)
