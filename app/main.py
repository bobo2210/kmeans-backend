"""Module providing Function to run Webserver/API """
import os
import json
import uuid
import threading
from urllib.parse import unquote
import pandas as pd
import redis
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.kmeans_methods import run_kmeans_one_k, run_kmeans_elbow
from app.utils import read_file, check_parameter

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

app = FastAPI()

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Allow all origins by setting allow_origins to  "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dictionary to store tasks, including status and results
tasks = {}

@app.post("/kmeans/")
async def kmeans_start(file: UploadFile,
                       k: int,
                       number_kmeans_runs: str = 10,
                       max_iterations:int = 300,
                       tolerance: float = 0.0001,
                       init: str = "k-means++",
                       algorithm: str = "lloyd",
                       centroids: str = None,
                       normalization: str= None):
    """
    Uploads a json or csv file, performs k-means, and returns the id of the task

    Args:
        Only k and file are mandatory

        file (UploadFile): The uploaded json or csv file.

        k (int): The number of clusters

        number_runs (int): The number of times the kmeans algorithm 
                            is performed with different initial centroid positions

        max_iterations (int): The maximal number of iterations
                               performed by the kmeans algorithm

        tolerance (float): The height of the frobenius norm which has to be 
                            fallen below in order for the kmeans algorithm to stop iterating

        init(str) ("k-means++", "random" or "centroids"): 
                                    The initialisation method of the centroids. 
                                    k-means++: Automatically choose best initial start centroids;
                                    random: randomly choose startpoint
                                    centroids: Use the provided centroids

        algorithm (str) ("lloyd", "elkan", "auto", "full")

        Centroids JSON string containing the array of arrays of the initial centroid positions

        normalization string containing the 

    Returns:
        dict: The Id of the task
              If the uploaded file is not a json or csv, an error message is returned.
    """

    result = read_file(file.file, file.filename)

    if isinstance(result, pd.DataFrame):
        dataframe = result
    else:
        raise HTTPException(status_code=400, detail= result)

    if number_kmeans_runs.isdigit():
        number_runs = int(number_kmeans_runs)
    else:
        number_runs = number_kmeans_runs

    if centroids is not None:
        try:
            centroids = json.loads(unquote(centroids))
        except json.JSONDecodeError as exception:
            raise HTTPException(status_code=400, detail= str(exception)) from exception

    error_message = check_parameter(centroids, number_runs, dataframe, k, k, init, algorithm, normalization)

    if error_message != "":
        raise HTTPException(status_code=400, detail= error_message)

    # Create a unique task ID
    task_id = str(uuid.uuid4())

    # Initialize the task with a "processing" status and an empty results list.
    tasks[task_id] = {
        "status": "processing",
        "method": "one_k",
        "json_result": {},
        "json_inertia": {},
        "message": ""}

    data_upload = {
        "status": "processing",
        "method": "one_k"}

    redis_client.hmset(task_id, data_upload)
    redis_client.expire(task_id,600)

    # Create a separate thread to run run_kmeans_one_k
    kmeans_thread = threading.Thread(target=run_kmeans_one_k, args=(
        redis_client,dataframe, task_id, tasks, k, number_runs, max_iterations, tolerance, init, algorithm, centroids, normalization))
    kmeans_thread.start()

    return {"TaskID": task_id}

@app.post("/elbow/")
async def elbow_start(file: UploadFile,
                       k_min: int,
                       k_max: int,
                       number_kmeans_runs: str = 10,
                       max_iterations:int = 300,
                       tolerance: float = 0.0001,
                       init: str = "k-means++",
                       algorithm: str = "lloyd",
                       centroids: str = None,
                       normalization: str= None):
    """
    Uploads a json or csv file, performs k-means for each k, and returns the id of the task

    Args:
        Only k and file are mandatory

        file (UploadFile): The uploaded json or csv file.

        k_min (int): The lowest number of clusters on which kmeans is supposed performed in order to evaluate its inertia

        k_max (int): The highest number of clusters on which kmeans is supposed performed in order to evaluate its inertia

        number_runs (int): The number of times the kmeans algorithm 
                            is performed with different initial centroid positions

        max_iterations (int): The maximal number of iterations
                               performed by the kmeans algorithm

        tolerance (float): The height of the frobenius norm which has to be 
                            fallen below in order for the kmeans algorithm to stop iterating

        init(str) ("k-means++", "random" or "centroids"): 
                                    The initialisation method of the centroids. 
                                    k-means++: Automatically choose best initial start centroids;
                                    random: randomly choose startpoint
                                    centroids: Use the provided centroids

        algorithm (str) ("lloyd", "elkan", "auto", "full"): "lloyd"


        Centroids JSON string containing the array of arrays of the initial centroid positions

    Returns:
        dict: The Id of the task
              If the uploaded file is not a json or csv, an error message is returned.
    """
    result = read_file(file.file, file.filename)
    if isinstance(result, pd.DataFrame):
        dataframe = result
    else:
        raise HTTPException(status_code=400, detail= result)

    if number_kmeans_runs.isdigit():
        number_runs = int(number_kmeans_runs)
    else:
        number_runs = number_kmeans_runs

    if centroids is not None:
        try:
            centroids = json.loads(unquote(centroids))
        except json.JSONDecodeError as exception:
            raise HTTPException(status_code=400, detail= str(exception)) from Exception

    error_message = check_parameter(centroids, number_runs, dataframe, k_min, k_max, init, algorithm, normalization)

    if error_message != "":
        raise HTTPException(status_code=400, detail= error_message)

    # Create a unique task ID
    task_id = str(uuid.uuid4())

    # Initialize the task with a "processing" status and an empty results list
    tasks[task_id] = {
        "status": "processing",
        "method": "elbow",
        "json_result": {},
        "json_inertia": {},
        "message": ""}

    data_upload = {
        "status": "processing",
        "method": "elbow",
  }

    redis_client.hmset(task_id,data_upload)

    # Create a separate thread to run run_kmeans_one_k
    kmeans_elbow_thread = threading.Thread(target=run_kmeans_elbow, args=(
        redis_client, dataframe, task_id, tasks, k_min, k_max, number_runs, max_iterations, tolerance, init, algorithm, centroids, normalization))
    kmeans_elbow_thread.start()
    # Convert the DataFrame to a JSON-serializable format
    return {"TaskID": task_id}



@app.get("/kmeans/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Returns the current status of a task

    Args:
        task_id: The ID of the task
        
    Returns:
        dict: A dictionary with the status of the task.
    """
    task_status=redis_client.hget(task_id,'status')
    if task_status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_status == "Bad Request":
        raise HTTPException(status_code=400, detail= tasks[task_id]["message"])
    return {"status": task_status}

@app.get("/kmeans/result/{task_id}")
async def get_task_result(task_id: str):
    """
    Gets the results of the k-means method

    Args:
        task_id: The ID of the regarded task
        
    Returns:
        array: An array with the results of the task.
    """

    task_status = redis_client.hget(task_id,'status')
    if task_status is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_status != "completed":
        if task_status == "Bad Request":
            raise HTTPException(status_code=400, detail= tasks[task_id]["message"])
        raise HTTPException(status_code=400, detail="Task result not available yet")

    task_method = redis_client.hget(task_id,'method')

    if task_method == "one_k":
        task_result = redis_client.hget(task_id,'json_result')
        return json.loads(task_result)
    if task_method == "elbow":
        task_inertias = redis_client.hget(task_id,'inertia_values')
        return json.loads(task_inertias)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
