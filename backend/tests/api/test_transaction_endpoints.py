from typing import List

import pytest
from core.models import Budget, Transaction
from rest_framework.response import Response


@pytest.mark.django_db
def test_fetching_list(client):
    response: Response = client.get(f"/api/transaction/")

    assert response.status_code == 200

    # check pagination
    expected_fields: List[str] = ["count", "next", "previous", "results"]
    assert all([field in response.data.keys() for field in expected_fields])

    # # check single item structure
    for item in response.data["results"]:
        assert all([field in item.keys() for field in ["id", "category", "value", "kind"]])
        assert item["kind"] in ["income", "expanse"]


@pytest.mark.django_db
def test_fetching_retrieve(client, user):
    transaction = Transaction.objects.filter(budget__user=user).first()
    response: Response = client.get(f"/api/transaction/{transaction.id}/")

    assert response.status_code == 200
    assert all([field in response.data.keys() for field in ["id", "category", "value", "kind"]])
