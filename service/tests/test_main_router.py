from fastapi.testclient import TestClient


def test_root_endpoint(test_client: TestClient) -> None:
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "OSTDependency backend"}
