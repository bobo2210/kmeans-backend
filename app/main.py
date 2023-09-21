"""Module providing Function to run Webserver/API """
import asyncio
from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException
import uvicorn
import pandas as pd
from sklearn.cluster import KMeans

app = FastAPI()

# Dictionary to store tasks, including status and results
tasks = {}


@app.post("/kmeans/")
async def kmeans_start(file: UploadFile, num_clusters: int = 2):
    """
    Uploads a CSV file, performs k-means, and returns an array with the clusters 

    Args:
        file (UploadFile): The uploaded CSV file.
        num_clusters (int): The number of clusters, default = 2
        
    Returns:
        dict: A dictionary containing the DataFrame with the CSV data.
              If the uploaded file is not a CSV, an error message is returned.
    """
    if file.filename.endswith(".csv"):
        # Read the CSV file directly with pandas
        dataframe = pd.read_csv(file.file)
        # Create a unique task ID
        task_id = len(tasks) + 1
        # Initialize the task with a "processing" status and an empty results list
        tasks[task_id] = {"status": "processing", "results": []}
        asyncio.create_task(run_kmeans_onek(dataframe, num_clusters, task_id))
        return {"TaskID": task_id}
    return {"error": "Die hochgeladene Datei ist keine CSV-Datei."}

async def run_kmeans_onek(dataframe, num_clusters, task_id):
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
    return {"status": task_status}

@app.get("/kmeans/result/{task_id}")
async def get_task_result(task_id: int):
    """
    Gets the results of the k-means method

    Args:
        task_id: The ID of the regarded task
        
    Returns:
        dict: A dictionary with the results of the task.
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task_result = tasks[task_id]["results"]
    if not task_result:
        raise HTTPException(status_code=404, detail="Task result not available yet")

    return {"result": task_result}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
