import uuid

import pytest
from fastapi.testclient import TestClient


class TestGetPlan:
    def test_get_plans(self, test_client: TestClient) -> None:
        response = test_client.get("/plans")
        assert response.status_code == 200
        data = response.json()
        assert len(data["plans"]) == 0


class TestCreatePlan:
    def test_create_plan(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}

        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == request_data["name"]

    def test_create_invalid_plan(self, test_client: TestClient) -> None:
        request_data = {
            "name": "Test Plan",
        }
        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 422


class TestDeletePlan:
    def test_delete_plan(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}

        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        plan_id = response.json()["id"]

        response = test_client.get("/plans")
        assert response.status_code == 200
        assert len(response.json()["plans"]) == 1

        response = test_client.delete(f"/plans/{plan_id}")
        assert response.status_code == 204

        response = test_client.get("/plans")
        assert response.status_code == 200
        assert len(response.json()["plans"]) == 0

    def test_delete_nonexisting_plan(self, test_client: TestClient) -> None:
        response = test_client.delete(f"/plans/{uuid.uuid4()}")
        assert response.status_code == 404


class TestBookmarkPlan:
    def test_bookmark_plan(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}
        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        plan_id = response.json()["id"]

        response = test_client.patch(f"/plans/bookmark/{plan_id}")
        assert response.status_code == 204

    def test_bookmark_plan_twice(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}
        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        plan_id = response.json()["id"]

        response = test_client.patch(f"/plans/bookmark/{plan_id}")
        assert response.status_code == 204
        response = test_client.patch(f"/plans/bookmark/{plan_id}")
        assert response.status_code == 204

    def test_bookmark_nonexisting_plan(self, test_client: TestClient) -> None:
        response = test_client.get("/plans")
        assert response.status_code == 200
        assert len(response.json()["plans"]) == 0

        response = test_client.patch(f"/plans/bookmark/{uuid.uuid4()}")
        assert response.status_code == 404


@pytest.mark.usefixtures("overwrite_session_dependency")
class TestBadDB:
    def test_get_plans(self, test_client: TestClient) -> None:
        response = test_client.get("/plans")
        assert response.status_code == 500

    def test_get_plan(self, test_client: TestClient) -> None:
        response = test_client.get("/plans/shared/testSlug")
        assert response.status_code == 500

    def test_create_plan(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}

        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 500

    def test_delete_plan(self, test_client: TestClient) -> None:
        response = test_client.delete(f"/plans/{uuid.uuid4()}")
        assert response.status_code == 500

    def test_update_plan(self, test_client: TestClient) -> None:
        request_data = {"content": "Test Content"}

        response = test_client.post(f"/plans/{uuid.uuid4()}/update", json=request_data)
        assert response.status_code == 500

    def test_get_plan_history(self, test_client: TestClient) -> None:
        response = test_client.get(f"/plans/history/{uuid.uuid4()}")
        assert response.status_code == 500


class TestPublicSlug:
    def test_get_plan_by_public_slug(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}

        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        public_slug = response.json()["public_slug"]

        response = test_client.get(f"/plans/shared/{public_slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == request_data["name"]
        assert data["content"] == request_data["content"]

    def test_get_nonexisting_plan(self, test_client: TestClient) -> None:
        response = test_client.get("/plans/shared/testSlug")
        assert response.status_code == 404


class TestPlanHistory:
    def test_get_plan_history(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}
        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        plan_id = response.json()["id"]

        response = test_client.get(f"/plans/history/{plan_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["plans"]) == 1

    def test_update_plan(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}
        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        plan_id = response.json()["id"]

        request_data = {"content": "New Test Content"}
        response = test_client.post(f"/plans/{plan_id}/update", json=request_data)
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == request_data["content"]

    def test_update_and_get_history(self, test_client: TestClient) -> None:
        request_data = {"name": "Test Plan", "content": "Test Content"}
        response = test_client.post("/plans", json=request_data)
        assert response.status_code == 201
        plan_id = response.json()["id"]

        request_data = {"content": "New Test Content"}
        response = test_client.post(f"/plans/{plan_id}/update", json=request_data)
        assert response.status_code == 201

        response = test_client.get(f"/plans/history/{plan_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["plans"]) == 2
        assert data["plans"][0]["content"] == "New Test Content"
        assert data["plans"][1]["content"] == "Test Content"
