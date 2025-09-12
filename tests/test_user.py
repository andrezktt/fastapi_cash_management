from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "testpassword",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_login():
    client.post(
        "/users/",
        json={
            "email": "login@example.com",
            "name": "Login User",
            "password": "password123"
        }
    )
    response = client.post(
        "/users/token",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"