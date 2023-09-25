"""Module providing Function to run Webserver/API """
import asyncio
import json
import logging
import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
import uvicorn
import pandas as pd
from kmeans_methods import run_kmeans_one_k

app = FastAPI()

logger = logging.getLogger(__name__)

# Dictionary to store tasks, including status and results
tasks = {}


@app.post("/kmeans/")
async def kmeans_start(file: UploadFile):
    """
    Uploads a json file, performs k-means, and returns the id of the task

    Args:
        file (UploadFile): The uploaded json file.
                           The file has to contain the params of the kmeans method
        
    Returns:
        dict: The Id of the task
              If the uploaded file is not a json, an error message is returned.
    """
    if file.filename.endswith(".json"):
        #json Datei öffnen
        with file.file as json_file:
            data = json.load(json_file)

        #Zugriff auf die Parameter für K-Means
        kmeans_parameters = data["kmeans_parameters"]
        centroids_start_json = data["centroids"]
        centroids_start = np.array([[centroid["x"], centroid["y"]] for centroid in centroids_start_json])

        # Zugriff auf die Datenpunkte
        data_points = data.get("data_points", [])
        # Erstellen eines  Pandas DataFrame
        dataframe = pd.DataFrame(data_points)
        # Create a unique task ID
        task_id = len(tasks) + 1
        # Initialize the task with a "processing" status and an empty results list
        tasks[task_id] = {"status": "processing", "results": [], "message": ""}

        asyncio.create_task(run_kmeans_one_k(dataframe, task_id, tasks, kmeans_parameters, centroids_start))

        return {"TaskID": task_id}
    raise HTTPException(status_code=400, detail="Datei ist keine json Datei")


@app.get("/kmeans/status/{task_id}")
async def get_task_status(task_id: int):
    """
    Returns the current status of a task

    Args:
        task_id: The ID of the task
        
    Returns:
        dict: A dictionary with the status of the task.
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task_status = tasks[task_id]["status"]
    if task_status == "Bad Request":
        raise HTTPException(status_code=400, detail= tasks[task_id]["message"])
    return {"status": task_status}

@app.get("/kmeans/result/{task_id}")
async def get_task_result(task_id: int):
    """
    Gets the results of the k-means method

    Args:
        task_id: The ID of the regarded task
        
    Returns:
        array: An array with the results of the task.
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task_status = tasks[task_id]["status"]
    task_result = tasks[task_id]["results"]
    if task_status != "completed":
        if task_status == "Bad Request":
            raise HTTPException(status_code=400, detail= tasks[task_id]["message"])
        else:
            raise HTTPException(status_code=400, detail="Task result not available yet")

    return {"result": task_result.tolist()}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
