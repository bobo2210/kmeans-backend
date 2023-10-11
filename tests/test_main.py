"""Module Testing with pytest"""
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient instance to interact with your FastAPI app
client = TestClient(app)

# Sample JSON data for testing
test_params = {
    "k": 2,
    "number_kmeans_runs": 5,
    "max_iterations": 300,
    "tolerance": 0.0001,
    "init": "k-means++",
    "algorithm": "lloyd"
}

# Pfad zur Datei, die du senden möchtest
TESTFILEPATH = "tests/kmeans_test.json"
WRONGFILEPATH = "tests/kmeans_test.error"

# Überprüfe den Dateipfad
if not os.path.exists(TESTFILEPATH):
    raise FileNotFoundError(f"File not found: {TESTFILEPATH}")


def test_upload_json_and_check_task_status():
    """test upload valid file and check response"""
    # Test uploading a JSON file
    with open(TESTFILEPATH, "rb") as file:
        response = client.post("/kmeans/",params=test_params,files={"file": file})

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

    # # Parse the response JSON
    # response_data = response.json()

    # # Check if the task status is "processing" initially
    # assert response_data["status"] == "processing"

def test_upload_invalid_file():
    """Test upload invalid file"""
    # Test uploading an invalid JSON file
    with open(WRONGFILEPATH, "rb") as file:
        response = client.post("/kmeans/",params=test_params,files={"file": file})

    # Check if the response status code is 400 Bad Request
    assert response.json() == {"error": "Die hochgeladene Datei ist keine json, xlsx oder csv Datei."}

def test_get_task_result():
    """Test get result"""
    # Test uploading a JSON file and retrieving task result
    with open(TESTFILEPATH, "rb") as file:
        response = client.post("/kmeans/",params=test_params,files={"file": file})

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

    # Add your assertions for the task result here
    # assert response_data["result"] == expected_result

if __name__ == "__main__":
    pytest.main()
