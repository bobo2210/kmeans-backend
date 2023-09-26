"""Main test"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """Test API"""
    response = client.get("/kmeans/status/2")
    assert response.json() == {"detail": "Task not found"}
