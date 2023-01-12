import pytest
from django.contrib.auth.models import User
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from tests.factories import TransactionCategoryFactory, TransactionFactory

register(TransactionCategoryFactory)
register(TransactionFactory)

CATEGORIES = ["food", "school", "tax", "home", "trip", "other"]


@pytest.fixture
def client():
    client = APIClient()
    user = User.objects.first()
    access = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client


@pytest.fixture(autouse=True)
def mock_objects(transaction_factory, transaction_category_factory):
    # Create categories
    for category in CATEGORIES:
        transaction_category_factory.create(name=category)
    # Create transactions
    for _ in range(10):
        transaction_factory.create()
