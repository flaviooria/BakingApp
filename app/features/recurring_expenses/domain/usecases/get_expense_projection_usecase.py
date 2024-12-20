from features.recurring_expenses.domain.repositories.recurring_expenses_repository import RecurringExpensesRepository


class GetExpenseProjectionUseCase:
    def __init__(self, expense_projection_repository: RecurringExpensesRepository):
        self.expense_projection_repository = expense_projection_repository

    def execute(self, user_id: int):
        return self.expense_projection_repository.get_expenses_projection(user_id)
