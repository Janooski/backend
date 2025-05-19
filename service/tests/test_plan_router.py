import uuid

from fastapi.testclient import TestClient


def test_get_plans(test_client: TestClient, get_valid_auth_header: dict[str, str]) -> None:
    header = get_valid_auth_header
    response = test_client.get("/api/plans", headers=header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 0


def test_get_plans_fails_without_authorization_token(test_client: TestClient) -> None:
    header = {"Authorization": "invalid_token"}

    response = test_client.get("/api/plans", headers=header)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

    response = test_client.get("/api/plans")
    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization header missing"}


def test_create_plan(test_client: TestClient, get_valid_auth_header: dict[str, str]) -> None:
    request_data = {"name": "Test Plan", "content": "Test COntent"}

    response = test_client.post("/api/plan", json=request_data, headers=get_valid_auth_header)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == request_data["name"]


def test_create_plan_fails_with_unprocessable_data(
    test_client: TestClient, get_valid_auth_header: dict[str, str]
) -> None:
    request_data = {
        "name": "Test Plan",
    }
    response = test_client.post("/api/plan", json=request_data, headers=get_valid_auth_header)
    assert response.status_code == 422


def test_delete_plan(test_client: TestClient, get_valid_auth_header: dict[str, str]) -> None:
    request_data = {"name": "Test Plan", "content": "Test COntent"}
    response = test_client.post("/api/plan", json=request_data, headers=get_valid_auth_header)
    assert response.status_code == 201
    data = response.json()
    plan_id = data["id"]

    response = test_client.get("/api/plans", headers=get_valid_auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 1

    response = test_client.delete(f"/api/plan/{plan_id}", headers=get_valid_auth_header)
    assert response.status_code == 204

    response = test_client.get("/api/plans", headers=get_valid_auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 0


def test_delete_nonexisting_plan(test_client: TestClient, get_valid_auth_header: dict[str, str]) -> None:
    request_data = {"name": "Test Plan", "content": "Test Content"}
    response = test_client.post("/api/plan", json=request_data, headers=get_valid_auth_header)
    assert response.status_code == 201

    response = test_client.get("/api/plans", headers=get_valid_auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 1

    response = test_client.delete(f"/api/plan/{uuid.uuid4()}", headers=get_valid_auth_header)
    assert response.status_code == 404

    response = test_client.get("/api/plans", headers=get_valid_auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 1


def test_bookmarkPlan(test_client: TestClient, get_valid_auth_header: dict[str, str]) -> None:
    request_data = {"name": "Test Plan", "content": "Test Content"}
    response = test_client.post("/api/plan", json=request_data, headers=get_valid_auth_header)
    assert response.status_code == 201
    data = response.json()
    plan_id = data["id"]

    response = test_client.put(f"/api/plan/bookmark/{plan_id}", headers=get_valid_auth_header)
    assert response.status_code == 200

    response = test_client.get("/api/plans", headers=get_valid_auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 1
    assert data["plans"][0]["bookmark"] is True

def test_bookmarkPlanTwice(test_client: TestClient, get_valid_auth_header: dict[str, str]) -> None:
    request_data = {"name": "Test Plan", "content": "Test Content"}
    response = test_client.post("/api/plan", json=request_data, headers=get_valid_auth_header)
    assert response.status_code == 201
    data = response.json()
    plan_id = data["id"]

    response = test_client.put(f"/api/plan/bookmark/{plan_id}", headers=get_valid_auth_header)
    assert response.status_code == 200
    response = test_client.put(f"/api/plan/bookmark/{plan_id}", headers=get_valid_auth_header)
    assert response.status_code == 200

    response = test_client.get("/api/plans", headers=get_valid_auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 1
    assert data["plans"][0]["bookmark"] is False