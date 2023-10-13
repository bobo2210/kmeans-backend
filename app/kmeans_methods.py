"""
Module for k-means clustering methods.
"""

import json
from sklearn.cluster import KMeans
from app.utils import dataframe_to_json_str, elbow_to_json
from app.datacheck import data_check

# pylint: disable=inconsistent-return-statements
def run_kmeans_one_k(dataframe,
                    task_id,
                    tasks,
                    k_value,
                    number_runs,
                    max_iterations,
                    tolerance,
                    initialisation,
                    used_algorithm,
                    centroids_start=None,
                    normalization=None):
    """
    Uploads a CSV file, performs k-means, and returns an array with the clusters 

    Args:
        dataframe (pd.DataFrame): The uploaded CSV data.
        num_clusters (int): The number of clusters, default = 2
        task_id (int): The taskID
        
    Returns:
        dict: A dictionary with the DataFrame with the CSV data.
              If the uploaded file is not a CSV, an error message is returned.
    """
    #Dateicheck einfuegen
    if tasks[task_id]["status"] != "Data prepared. Processing...":
        tasks[task_id]["status"] = "Preparing Data..."
        dataframe = data_check(dataframe, tasks, task_id, normalization)

    if dataframe is None:
        return

    kmeans = None
    if initialisation in ("k-means++","random"):
        # Instantiate sklearn's k-means using num_clusters clusters
        kmeans = KMeans(
            n_clusters=k_value,
            init=initialisation,
            n_init=number_runs,
            max_iter=max_iterations,
            tol=tolerance,
            algorithm=used_algorithm,
            verbose=2)
    elif initialisation == "centroids":
        # Instantiate sklearn's k-means using num_clusters clusters
        kmeans = KMeans(
                n_clusters=k_value,
                init=centroids_start,
                n_init=number_runs,
                max_iter=max_iterations,
                tol=tolerance,
                algorithm=used_algorithm,
                verbose=2)
    if kmeans is None:
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str(initialisation)
        return
    try:
        # execute k-means algorithm
        kmeans.fit(dataframe.values)
        # Update the task with the "completed" status and the results
        if tasks[task_id]["method"] == "one_k":
            result_to_json = dataframe_to_json_str(dataframe, kmeans.labels_, kmeans.cluster_centers_)
            json_string = json.loads(result_to_json)
            tasks[task_id]["json_result"] = json_string
            tasks[task_id]["status"] = "completed"
        elif  tasks[task_id]["method"] == "elbow":
            return kmeans.inertia_
    except ValueError as exception:
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str(exception)


def run_kmeans_elbow(dataframe,
                        task_id,
                        tasks,
                        k_min,
                        k_max,
                        number_runs,
                        max_iterations,
                        tolerance,
                        initialisation,
                        used_algorithm,
                        centroids_start=None,
                        normalization=None):
    """
    Performs kmeans for elbow method
    """

    k_min = max(k_min, 1)
    k_values = range(k_min, k_max + 1)
    inertia_values = []

    for k_value in k_values:
        inertia = run_kmeans_one_k(dataframe,
                                    task_id,
                                    tasks,
                                    k_value,
                                    number_runs,
                                    max_iterations,
                                    tolerance,
                                    initialisation,
                                    used_algorithm,
                                    centroids_start,
                                    normalization)
        inertia_values.append(inertia)

    elbow_json = elbow_to_json(k_min, k_max, inertia_values)
    json_string = json.loads(elbow_json)
    tasks[task_id]["json_inertia"] = json_string
    tasks[task_id]["status"] = "completed"
