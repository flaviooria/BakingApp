from abc import ABC, abstractmethod

from app.common.functions import Either
from app.exceptions import ApiException


class RecurringExpensesRepository(ABC):
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
