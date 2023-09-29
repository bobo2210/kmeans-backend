"""Module Tests App"""
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient instance to interact with your FastAPI app
client = TestClient(app)

# Sample JSON data for testing
sample_json_data = {
    "kmeans_parameters": {"n_clusters": 2},
    "centroids": [{"x": 1, "y": 2}, {"x": 3, "y": 4}],
    "data_points": [{"x": 1, "y": 2}, {"x": 3, "y": 4}],
}
def test_upload_json_and_check_task_status():
    """Test json upload"""
    # Test uploading a JSON file
    response = client.post("/kmeans/", files={"file": ("data.json", json.dumps(sample_json_data))})

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check if the response contains a task ID
    assert "TaskID" in response_data

    task_id = response_data["TaskID"]

    # Check the status of the task
    response = client.get(f"/kmeans/status/{task_id}")

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check if the task status is "processing" initially
    assert response_data["status"] == "processing"

def test_upload_invalid_file():
    """Test upload invalid file"""
    # Test uploading a non-JSON file
    response = client.post("/kmeans/", files={"file": ("data.txt", "This is not JSON data")})

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check if an error message is returned
    assert "error" in response_data

def test_get_task_result():
    """Test get task result"""
    # Test getting task result
    response = client.post("/kmeans/", files={"file": ("data.json", json.dumps(sample_json_data))})

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check if the response contains a task ID
    assert "TaskID" in response_data

    task_id = response_data["TaskID"]

    # Poll for task completion
    while True:
        response = client.get(f"/kmeans/status/{task_id}")
        response_data = response.json()
        if response_data["status"] == "completed":
            break

    # Get task result
    response = client.get(f"/kmeans/result/{task_id}")

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check if the result is as expected (you may need to modify
    # this based on your application's behavior)
    # assert response_data["result"] == expected_result

if __name__ == "__main__":
    pytest.main()


#"""Main test"""
#from fastapi.testclient import TestClient
#from app.main import app
#
#client = TestClient(app)
#
#def test_read_main():
#    """Test API"""
#    response = client.get("/kmeans/status/2")
#    assert response.json() == {"detail": "Task not found"}
