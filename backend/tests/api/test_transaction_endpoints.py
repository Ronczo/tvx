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


@pytest.mark.django_db
def test_delete(client, transaction_factory):
    factory_to_delete = transaction_factory()
    total_amount = Transaction.objects.all().count()
    response: Response = client.delete(f"/api/transaction/{factory_to_delete.id}/")
    assert response.status_code == 204
    assert Transaction.objects.all().count() == total_amount - 1


@pytest.mark.parametrize(
    "kind_type",
    ["income", "expanse", "something"],
)
@pytest.mark.django_db
def test_post(client, user, kind_type):
    budget = Budget.objects.filter(user=user).first()
    payload = {"category": "my_category", "kind": kind_type, "budget": budget.id}
    total_amount = Transaction.objects.all().count()
    response: Response = client.post(f"/api/transaction/", payload)
    print("ddd", response.data)
    if kind_type != "something":
        assert response.status_code == 201
        assert total_amount + 1 == Transaction.objects.all().count()
    else:
        assert response.status_code == 400
        assert total_amount == Transaction.objects.all().count()
