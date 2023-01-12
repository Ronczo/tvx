import pytest
from core.models import Budget, Transaction, TransactionType


@pytest.mark.django_db
def test_budget_balance():
    budget = Budget.objects.filter(transactions__isnull=False).first()

    # I know I could use aggregate, but I didn't want to test looks like method :)
    income_transactions = Transaction.objects.filter(budget=budget, kind=TransactionType.IN)
    sum_incomes = sum([transaction.value for transaction in income_transactions])

    expanse_transactions = Transaction.objects.filter(budget=budget, kind=TransactionType.EX)
    sum_expanses = sum([transaction.value for transaction in expanse_transactions])

    assert sum_incomes - sum_expanses == budget.budget_balance
