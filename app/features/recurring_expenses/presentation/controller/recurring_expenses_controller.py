from flask import Blueprint, request, jsonify

from common.middleware.auth_middleware import AuthMiddleware
from entities.entities import User
from features.recurring_expenses.data.database.recurring_expense_database import RecurringExpensesImpl
from features.recurring_expenses.data.repositories.recurring_expense_repository_impl import \
    RecurringExpensesRepositoryImpl
from features.recurring_expenses.domain.usecases.create_expenses_usecase import CreateRecurringExpenseUseCase
from features.recurring_expenses.domain.usecases.delete_expense_usecase import DeleteRecurringExpenseUseCase
from features.recurring_expenses.domain.usecases.get_expense_projection_usecase import GetExpenseProjectionUseCase
from features.recurring_expenses.domain.usecases.get_expenses_usecase import GetRecurringExpensesUseCase
from features.recurring_expenses.domain.usecases.update_expenses_usecase import UpdateRecurringExpenseUseCase
from shared.handle_api_error import handle_msg_error

recurring_expenses_router = Blueprint("expenses", __name__)

recurring_expenses_impl = RecurringExpensesImpl()
recurring_expenses_repository = RecurringExpensesRepositoryImpl(recurring_expenses_impl)
create_expense_use_case = CreateRecurringExpenseUseCase(recurring_expenses_repository)
get_expenses_use_case = GetRecurringExpensesUseCase(recurring_expenses_repository)
update_expense_use_case = UpdateRecurringExpenseUseCase(recurring_expenses_repository)
delete_expense_use_case = DeleteRecurringExpenseUseCase(recurring_expenses_repository)
get_expense_projection_use_case = GetExpenseProjectionUseCase(recurring_expenses_repository)


@recurring_expenses_router.get("/recurring-expenses", endpoint="get_recurring_expenses")
@AuthMiddleware.auth_required
def get_recurring_expenses(current_user: User):
    try:
        result = get_expenses_use_case.execute(current_user.id)

        return result.fold(handle_msg_error, lambda expenses: (jsonify(expenses), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500


@recurring_expenses_router.post("/recurring-expenses", endpoint="create_recurring_expense")
@AuthMiddleware.auth_required
def create_recurring_expense(current_user: User):
    try:
        body = request.get_json()

        body.update({"user_id": current_user.id})

        result = create_expense_use_case.execute(body)

        return result.fold(handle_msg_error, lambda expense: (
            jsonify({"msg": "Recurring expense added successfully.", "data": expense}), 201))
    except Exception as ex:
        return jsonify(str(ex)), 500


@recurring_expenses_router.put("/recurring-expenses/<int:expense_id>", endpoint="update_recurring_expense")
@AuthMiddleware.auth_required
def update_expenses(_: User, expense_id: int):
    try:
        body = request.get_json()

        result = update_expense_use_case.execute(expense_id, body)

        return result.fold(handle_msg_error, lambda expense: (
            jsonify({"msg": "Recurring expense updated successfully.", "data": expense}), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500


@recurring_expenses_router.delete("/recurring-expenses/<int:expense_id>", endpoint="delete_recurring_expense")
@AuthMiddleware.auth_required
def delete_expenses(_: User, expense_id: int):
    try:
        result = delete_expense_use_case.execute(expense_id)

        return result.fold(handle_msg_error,
                           lambda _: (jsonify({"msg": "Recurring expense deleted successfully."}), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500


@recurring_expenses_router.get("/recurring-expenses/projection", endpoint="get_expense_projection")
@AuthMiddleware.auth_required
def get_projection(user: User):
    try:
        result = get_expense_projection_use_case.execute(user.id)

        return result.fold(handle_msg_error, lambda projection: (jsonify(projection), 200))
    except Exception as ex:
        return jsonify(str(ex)), 500
