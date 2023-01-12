import pytest
from django.contrib.auth.models import User
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from tests.factories import BudgetFactory, TransactionCategoryFactory, TransactionFactory

register(TransactionCategoryFactory)
register(TransactionFactory)
register(BudgetFactory)

CATEGORIES = ["food", "school", "tax", "home", "trip", "other"]


@pytest.fixture
def client(user):
    client = APIClient()
    access = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client


@pytest.fixture(autouse=True)
def mock_objects(transaction_factory, transaction_category_factory):
    # Create categories
    [transaction_category_factory.create(name=category) for category in CATEGORIES]
    # Create transactions
    transaction_factory.create_batch(10)


@pytest.fixture()
def user():
    return User.objects.last()
