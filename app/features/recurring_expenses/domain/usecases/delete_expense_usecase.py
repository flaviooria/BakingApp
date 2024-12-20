from features.recurring_expenses.domain.repositories.recurring_expenses_repository import RecurringExpensesRepository


class DeleteRecurringExpenseUseCase:
    def __init__(self, recurring_exp_repository: RecurringExpensesRepository):
        self.recurring_exp_repository = recurring_exp_repository

    def execute(self, expense_id: int):
        return self.recurring_exp_repository.delete_expense(expense_id)
