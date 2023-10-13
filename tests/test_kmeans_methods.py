"""
    Testing kmeans methods with pylint
"""
import pandas as pd
from app.kmeans_methods import run_kmeans_one_k

# pylint: disable=unused-variable
def test_valid_input_kmeans_plusplus():
    """
    Test valid input
    """
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })

    tasks = {}
    tasks[1] = {
        "status": "processing",
        "method": "one_k",
        "Datenpunkte": data,
        "json_result": {},
        "inertia_values": [],
        "message": ""}

    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="k-means++", used_algorithm="auto")
    assert tasks[task_id]["status"] == "completed"
    assert "json_result" in tasks[task_id]

# pylint: disable=unused-variable
def test_valid_input_random_initialization():
    """
    Test random initialisation
    """
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })

    tasks = {}
    tasks[1] = {
        "status": "processing",
        "method": "one_k",
        "Datenpunkte": data,
        "json_result": {},
        "inertia_values": [],
        "message": ""}

    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=3,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="random", used_algorithm="full")
    assert tasks[task_id]["status"] == "completed"
    assert "json_result" in tasks[task_id]

# pylint: disable=unused-variable
def test_valid_input_centroids_initialization():
    """
    Test valid input for centroids
    """
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })
    centroids_start = [[1, 5], [5, 1]]

    tasks = {}
    tasks[1] = {
        "status": "processing",
        "method": "one_k",
        "Datenpunkte": data,
        "json_result": {},
        "inertia_values": [],
        "message": ""}

    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="centroids", used_algorithm="auto",
                              centroids_start=centroids_start)
    assert tasks[task_id]["status"] == "completed"
    assert "json_result" in tasks[task_id]

# pylint: disable=unused-variable
def test_invalid_initialization_method():
    """
    Test invalid initialisation
    """
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })

    tasks = {}
    tasks[1] = {
        "status": "processing",
        "method": "one_k",
        "Datenpunkte": data,
        "json_result": {},
        "inertia_values": [],
        "message": ""}

    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="invalid_method", used_algorithm="full")
    assert tasks[task_id]["status"] == "Bad Request"

# pylint: disable=unused-variable
def test_invalid_data():
    """
    Test invalid data
    """
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })

    tasks = {}
    tasks[1] = {
        "status": "processing",
        "method": "one_k",
        "Datenpunkte": data,
        "json_result": {},
        "inertia_values": [],
        "message": ""}

    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="k-means++", used_algorithm="false")
    assert tasks[task_id]["status"] == "Bad Request"
