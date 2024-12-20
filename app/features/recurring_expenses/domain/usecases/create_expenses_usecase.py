from features.recurring_expenses.domain.repositories.recurring_expenses_repository import RecurringExpensesRepository


class CreateRecurringExpenseUseCase:

    def __init__(self, recurring_exp_repository: RecurringExpensesRepository):
        self.recurring_exp_repository = recurring_exp_repository

    def execute(self, new_expense: dict):
        return self.recurring_exp_repository.create(new_expense)
