from typing import List

import pytest
from django.db.models import Q
from rest_framework.response import Response

from core.models import Budget


@pytest.mark.django_db
def test_fetching_list(client):
    response: Response = client.get(f"/api/budget/")

    assert response.status_code == 200

    # check pagination
    expected_fields: List[str] = ["count", "next", "previous", "results"]
    assert all([field in response.data.keys() for field in expected_fields])

    # check single item structure
    for item in response.data["results"]:
        assert all(
            [
                field in item.keys()
                for field in ["id", "transactions", "balance", "user", "name"]
            ]
        )

    # check filtering
    amount_without_filter = response.data["count"]
    response_with_filter: Response = client.get(f"/api/budget/?category=food")
    assert response_with_filter.data["count"] != amount_without_filter


@pytest.mark.django_db
def test_fetching_retrieve(client, user):
    budget = Budget.objects.filter(user=user).first()
    response: Response = client.get(f"/api/budget/{budget.id}/")

    assert response.status_code == 200

    # check single item structure
    assert all(
        [
            field in response.data.keys()
            for field in ["id", "transactions", "balance", "user", "name"]
        ]
    )

    # check permissions
    another_budget = Budget.objects.filter(~Q(user=user)).first()
    response_another_budget: Response = client.get(f"/api/budget/{another_budget.id}/")
    assert response_another_budget.status_code == 403


@pytest.mark.django_db
def test_delete(client, budget_factory):
    budget_to_delete = budget_factory()
    total_amount = Budget.objects.all().count()
    response: Response = client.delete(f"/api/budget/{budget_to_delete.id}/")
    assert response.status_code == 204
    assert Budget.objects.all().count() == total_amount - 1


@pytest.mark.django_db
def test_patch(client, budget_factory):
    budget_to_edit = budget_factory()
    payload = {"name": "new_name"}
    response: Response = client.patch(f"/api/budget/{budget_to_edit.id}/", payload)
    assert response.status_code == 200
    budget = Budget.objects.get(id=budget_to_edit.id)
    assert budget.name == payload["name"]


@pytest.mark.django_db
def test_post(client, user):
    payload = {"name": "test", "user": user.id}
    total_amount = Budget.objects.all().count()
    response: Response = client.post(f"/api/budget/", payload)
    assert response.status_code == 201
    assert total_amount + 1 == Budget.objects.all().count()


@pytest.mark.django_db
def test_my_budgets(client, user):
    response: Response = client.get(f"/api/budget/my-budgets/")

    assert response.status_code == 200

    # check pagination
    expected_fields: List[str] = ["count", "next", "previous", "results"]
    assert all([field in response.data.keys() for field in expected_fields])

    # check single item structure
    for item in response.data["results"]:
        assert all(
            [
                field in item.keys()
                for field in ["id", "transactions", "balance", "user", "name"]
            ]
        )
        # Check if every budget belongs to user
        budget = Budget.objects.get(id=item["id"])
        assert budget.user.id == user.id


@pytest.mark.django_db
def test_share(client, user, budget_factory):
    new_budget = budget_factory()

    payload = {"user": user.id, "budget": new_budget.id}
    response: Response = client.post(f"/api/budget/share/", payload)

    assert response.status_code == 200
    assert response.data == f"Budget shared with user {user.username}"
    assert user in new_budget.allowed_to.all()


@pytest.mark.django_db
def test_shared_with_me(client, user):
    response: Response = client.get(f"/api/budget/shared-with-me/")

    # check pagination
    expected_fields: List[str] = ["count", "next", "previous", "results"]
    assert all([field in response.data.keys() for field in expected_fields])

    # check single item structure
    for item in response.data["results"]:
        assert all(
            [
                field in item.keys()
                for field in ["id", "transactions", "balance", "user", "name"]
            ]
        )
        # Check if every budget bis shared with user
        budget = Budget.objects.get(id=item["id"])
        assert user in budget.allowed_to.all()

    assert response.status_code == 200
