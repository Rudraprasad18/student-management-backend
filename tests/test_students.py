from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "FastAPI + PostgreSQL is working!"


def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_nonexistent_student():
    response = client.put(
        "/students/999999",
        json={
            "name": "Nobody",
            "branch": "Test",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_delete_nonexistent_student():
    response = client.delete("/students/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"