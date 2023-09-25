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
    return {"error": "Die hochgeladene Datei ist keine json-Datei."}

async def data_check(dataframe):
    """
    Checks a dataframe and clears it for clustering 

    Args:
        dataframe (pd.DataFrame): The uploaded CSV data.
        cleaned_df (pd.DataFrame): The cleaned CSV data.
        
    Returns:
        cleaned_df (pd.DataFrame): The cleaned CSV data.
    """
    cleaned_df=dataframe.dropna()
    for column in cleaned_df.columns:
        if contains_numbers_and_letters(cleaned_df[column]).any():
            cleaned_df.drop(column, axis=1, inplace=True)
    return cleaned_df

async def contains_numbers_and_letters(column):
    """
    Checks if a column contains only numbers or letters 
        
    Returns:
        bool for check
    """
    return column.str.contains(r'[0-9]') & column.str.contains(r'[a-zA-Z]')

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
        raise HTTPException(status_code=400, detail="Task result not available yet")

    return {"result": task_result.tolist()}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)

async def dataframe_to_json(currenttaskid, dataframe1, dataframe2):
    """
    merges two dataframes to a json with the current id in the name 
        
    Returns:
        json for frontend
    """
    # JSON erstellen
    filename = 'data'+str(currenttaskid)
    fileend = '.json'
    output_file = filename + fileend
    # Erstes DataFrame in JSON speichern (Überschreiben, falls die Datei existiert)
    dataframe1.to_json(output_file, orient='records')
    # Zweites DataFrame in JSON speichern (Anhängen, falls die Datei existiert)
    dataframe2.to_json(output_file, orient='records', lines=True, mode='a')
    # return JSON
    return output_file
