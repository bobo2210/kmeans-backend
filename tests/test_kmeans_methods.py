import pandas as pd
from your_module import run_kmeans_one_k

def test_valid_input_kmeans_plusplus():
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })
    tasks = {}
    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="k-means++", used_algorithm="auto")
    assert tasks[task_id]["status"] == "completed"
    assert "json_result" in tasks[task_id]
    assert tasks[task_id]["json_result"]["n_clusters"] == 2

def test_valid_input_random_initialization():
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })
    tasks = {}
    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=3,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="random", used_algorithm="full")
    assert tasks[task_id]["status"] == "completed"
    assert "json_result" in tasks[task_id]
    assert tasks[task_id]["json_result"]["n_clusters"] == 3

def test_valid_input_centroids_initialization():
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })
    centroids_start = [[1, 5], [5, 1]]
    tasks = {}
    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="centroids", used_algorithm="auto",
                              centroids_start=centroids_start)
    assert tasks[task_id]["status"] == "completed"
    assert "json_result" in tasks[task_id]
    assert tasks[task_id]["json_result"]["n_clusters"] == 2

def test_invalid_initialization_method():
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 4, 3, 2, 1]
    })
    tasks = {}
    task_id = 1
    result = run_kmeans_one_k(data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="invalid_method", used_algorithm="full")
    assert tasks[task_id]["status"] == "Bad Request"

def test_invalid_data():
    invalid_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5]})
    tasks = {}
    task_id = 1
    result = run_kmeans_one_k(invalid_data, task_id, tasks, k_value=2,
                              number_runs=5, max_iterations=100, tolerance=1e-4,
                              initialisation="k-means++", used_algorithm="auto")
    assert tasks[task_id]["status"] == "Bad Request"
