from features.recurring_expenses.domain.repositories.recurring_expenses_repository import RecurringExpensesRepository


class GetRecurringExpensesUseCase:
    def __init__(self, recurring_exp_repository: RecurringExpensesRepository):
        self.recurring_exp_repository = recurring_exp_repository

    def execute(self, user_id: int):
        return self.recurring_exp_repository.get_recurring_expenses(user_id)
