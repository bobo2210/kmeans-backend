"""
Module for k-means clustering methods.
"""

from sklearn.cluster import KMeans

async def run_kmeans_one_k(dataframe, task_id, tasks, kmeans_parameters, centroids_start=None):
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

    #get the different params
    k_value = kmeans_parameters["k"]
    number_runs = kmeans_parameters["number_runs"]
    maximum_iter = kmeans_parameters["max_iterations"]
    tolerance = kmeans_parameters["tolerance"]
    #distance_nominal = kmeans_parameters["distance_nominal"]
    #distance_cardinal = kmeans_parameters["distance_cardinal"]
    initialisation = kmeans_parameters["init"]
    used_algorithm = kmeans_parameters["algorithm"]
    error_message = ""
    if not isinstance(number_runs, int):
        error_message += "The Number of runs has to be an integer. "
    if not isinstance(tolerance, float):
        error_message += "The tolerance has to be a float value. "
    if not isinstance(maximum_iter, int):
        error_message += "The maximal number of iterations has to be an integer. "
    if not isinstance(number_runs, int) and number_runs != 'auto':
        error_message += "The number of kmeans-runs has to be an integer. "
    if k_value > len(dataframe) or not isinstance(k_value, int):
        error_message += ("The k-value has to be an integer"
                          " and smaller than the number of datapoints. ")
    if initialisation in ("k-means++","random"):
        # Instantiate sklearn's k-means using num_clusters clusters
        kmeans = KMeans(
            n_clusters=k_value,
            init=initialisation,
            n_init=number_runs,
            max_iter=maximum_iter,
            tol=tolerance,
            algorithm=used_algorithm,
            verbose=2)
    elif initialisation == "cluster":
        # Instantiate sklearn's k-means using num_clusters clusters
        kmeans = KMeans(
            n_clusters=k_value,
            init=centroids_start,
            n_init=number_runs,
            max_iter=maximum_iter,
            tol=tolerance,
            algorithm=used_algorithm,
            verbose=2)
    else:
        error_message += ("The parameter init has to be k-means++, random or cluster"
                          " in combination with a specification"
                          " of the initial centroid positions. ")
    if error_message != "":
        tasks[task_id]["status"] = "Bad Request"
        tasks[task_id]["message"] = error_message
        return

    # execute k-means algorithm
    kmeans.fit(dataframe.values)
    # Update the task with the "completed" status and the results
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["results"] = kmeans.labels_
