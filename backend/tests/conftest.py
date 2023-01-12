import pytest
from django.contrib.auth.models import User
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from tests.factories import (
    BudgetFactory,
    TransactionCategoryFactory,
    TransactionFactory,
    UserFactory,
)

register(TransactionCategoryFactory)
register(UserFactory)
register(BudgetFactory)
register(TransactionFactory)


@pytest.fixture
def client():
    client = APIClient()
    user = User.objects.first()
    access = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client


@pytest.fixture()
def user():
    user = User.objects.first()
    access = AccessToken.for_user(user)
    return (user, access)


@pytest.fixture(autouse=True)
def db_imitation(user_factory, budget_factory, transaction_factory):
    # Create users.
    for _ in range(21):
        user_factory.create()
    # Create budgets
    for _ in range(30):
        budget_factory.create()
    # Create transactions
    for _ in range(100):
        transaction_factory.create()
