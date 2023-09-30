"""
Module for k-means clustering methods.
"""

from sklearn.cluster import KMeans

# pylint: disable=too-many-arguments
def run_kmeans_one_k(dataframe,
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
        task_id (int): The task ID
        
    Returns:
        dict: A dictionary with the DataFrame with the CSV data.
              If the uploaded file is not a CSV, an error message is returned.
    """
    #Dateicheck einfuegen
    #dataframe_clean = main.data_check(dataframe)

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
    try:
        # execute k-means algorithm
        kmeans.fit(dataframe.values)
        # Update the task with the "completed" status and the results
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["results"] = kmeans.labels_
        tasks[task_id]["centroid_positions"] = kmeans.cluster_centers_
    except ValueError as exception:
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] += str(exception)
