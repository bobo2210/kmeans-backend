"""
Module for k-means clustering methods.
"""

import pandas as pd
from sklearn.cluster import KMeans

async def run_kmeans_one_k(dataframe, num_clusters, task_id, tasks):
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
    # Instantiate sklearn's k-means using num_clusters clusters
    kmeans = KMeans(n_clusters=num_clusters, n_init='auto', verbose=2)

    # execute k-means algorithm
    kmeans.fit(dataframe.values)
    # Update the task with the "completed" status and the results
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["results"] = kmeans.labels_

    # Return the cluster labels as a Series
    return pd.Series(kmeans.labels_)
