def test_get_plans(test_client):
    response = test_client.get("/api/plans")
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 0

def test_create_plan(test_client):
    request_data = {
        "name": "Test Plan",
        "content": "Test COntent"
    }
    response = test_client.post("/api/plan", json=request_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == request_data["name"]

def test_delete_plan(test_client):
    request_data = {
        "name": "Test Plan",
        "content": "Test COntent"
    }
    response = test_client.post("/api/plan", json=request_data)
    assert response.status_code == 201
    data = response.json()
    plan_id = data["id"]

    response = test_client.get("/api/plans")
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 1

    response = test_client.delete(f"/api/plan/{plan_id}")
    assert response.status_code == 204

    response = test_client.get("/api/plans")
    assert response.status_code == 200
    data = response.json()
    assert len(data["plans"]) == 0