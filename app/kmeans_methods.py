"""
Module for k-means clustering methods.
"""
import json
from sklearn.cluster import KMeans
from app.utils import dataframe_to_json_str
#from app.datacheck import data_check

# pylint: disable=too-many-arguments,inconsistent-return-statements, line-too-long
def run_kmeans_one_k(redis_client,
                    dataframe,
                    task_id,
                    tasks,
                    k_value,
                    number_runs,
                    max_iterations,
                    tolerance,
                    initialisation,
                    used_algorithm,
                    centroids_start=None):
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
    #dataframe = main.data_check(dataframe, tasks, taskid)

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
        tasks[task_id]["message"] = str(initialisation)
        redis_client.hset(task_id,'message',str(initialisation))
        redis_client.hset(task_id,'status',"Bad Request")


    try:
        # execute k-means algorithm
        kmeans.fit(dataframe.values)
        # Update the task with the "completed" status and the results
        if tasks[task_id]["method"] == "one_k":
            tasks[task_id]["status"] = "completed"
            result_to_json = dataframe_to_json_str(dataframe, kmeans.labels_, kmeans.cluster_centers_)
            json_string = json.loads(result_to_json)
            tasks[task_id]["json_result"] = json_string
            print(result_to_json)
            redis_client.hset(task_id,"json_result",str(result_to_json))
            redis_client.hset(task_id,"status","completed")
        elif  tasks[task_id]["method"] == "elbow":
            return kmeans.inertia_
    except ValueError as exception:
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str(exception)
        redis_client.hset(task_id,'message',str(exception))
        redis_client.hset(task_id,'status',"Bad Request")

# pylint: disable=too-many-locals
def run_kmeans_elbow(redis_client,
                        dataframe,
                        task_id,
                        tasks,
                        k_min,
                        k_max,
                        number_runs,
                        max_iterations,
                        tolerance,
                        initialisation,
                        used_algorithm,
                        centroids_start=None):
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
                                    centroids_start)
        inertia_values.append(inertia)

    tasks[task_id]["status"] = "completed"
    tasks[task_id]["inertia_values"] = inertia_values
    redis_client.hset(task_id,'inertia_values',inertia_values)
    redis_client.hset(task_id,'status',"completed")
