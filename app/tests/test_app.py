import pytest
from app.src.models import User

def test_health_endpoint(test_client):
    """
    Test the health check endpoint.
    """
    response = test_client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_user_model_logic():
    """
    Test simple model logic (Unit Test).
    """
    user = User(name="TestUser", email="test@example.com")
    assert user.name == "TestUser"
    assert "TestUser" in repr(user)

def test_index_route(test_client):
    """
    Test the index route.
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert "Hello from Flask" in response.json['message']
