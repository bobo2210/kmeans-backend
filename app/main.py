"""Module providing Function to run Webserver/API """
import asyncio
import json
import numpy as np
from fastapi import FastAPI, UploadFile, Form
from fastapi.exceptions import HTTPException
import uvicorn
import pandas as pd
import uuid
import io
from kmeans_methods import run_kmeans_one_k
from typing import Optional
from urllib.parse import unquote

app = FastAPI()

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
                       centroids: str = None):
    """
    Uploads a json or csv file, performs k-means, and returns the id of the task

    Args:
        Only k and file are mandatory
        file (UploadFile): The uploaded json or csv file.

        k (int): The number of clusters

        number_runs (int): The number of times the kmeans algorithm is performed with different initial centroid positions

        max_iterations (int): The maximal number of iterations performed by the kmeans algorithm

        tolerance (float): The height of the frobenius norm which has to be fallen below in order for the kmeans algorithm to stop iterating

        init(str) ("k-means++", "random" or "centroids"): The initialisation method of the centroids. 
                                                            k-means++: Automatically choose best initial start centroids;
                                                            random: randomly choose startpoint
                                                            centroids: Use the provided centroids

        algorithm (str) ("lloyd", "elkan", "auto", "full"): "lloyd"

        Centroids JSON string containing the array of arrays of the initial centroid positions

    Returns:
        dict: The Id of the task
              If the uploaded file is not a json or csv, an error message is returned.
    """

    if file.filename.endswith(".json"):

        #json Datei öffnen
        with file.file as json_file:
            data = json.load(json_file)

        #Zugriff auf die Centroids für K-Means
        centroids_start = data.get("centroids", None)

        # Zugriff auf die Datenpunkte
        data_points = data.get("data_points", [])

        # Erstellen eines  Pandas DataFrame
        dataframe = pd.DataFrame(data_points)
    elif file.filename.endswith(".csv"):
        centroids_start = None
        # Read the uploaded CSV file
        csv_data = await file.read()
        # Create a DataFrame from the CSV data
        dataframe = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), sep=";", usecols=range(1,3))
    else:
        return {"error": "Die hochgeladene Datei ist keine json oder csv Datei."}

    if number_kmeans_runs.isdigit():
        number_runs = int(number_kmeans_runs)
    else:
        number_runs = number_kmeans_runs

    if centroids is not None:
        try:
            centroids_start = json.loads(unquote(centroids))
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail= str(e))

    error_message = ""
    if not isinstance(number_runs, int) and number_runs != 'auto':
        error_message += "The number of kmeans-runs has to be an integer or ""auto"""
    if k > len(dataframe) or not isinstance(k, int):
        error_message += ("The k-value has to be an integer"
                          " and smaller than the number of datapoints. ")
    if (not init in ("k-means++","random", "centroids") or
        (init == "centroids" and (centroids is None and centroids_start is None))):
        error_message += ("The parameter init has to be k-means++, random or centroids"
                          " in combination with a specification"
                          " of the initial centroid positions. ")
    if error_message != "":
        raise HTTPException(status_code=400, detail= error_message)

    # Create a unique task ID
    task_id = str(uuid.uuid4())

    # Initialize the task with a "processing" status and an empty results list
    tasks[task_id] = {
        "status": "processing",
        "Datenpunkte": dataframe,
        "results": [],
        "centroid_positions": [],
        "message": ""}

    asyncio.create_task(run_kmeans_one_k(dataframe,
                                            task_id,
                                            tasks,
                                            k,
                                            number_runs,
                                            max_iterations,
                                            tolerance,
                                            init,
                                            algorithm,
                                            centroids_start))

    return {"TaskID": task_id}
    

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

def check_file(dataframe):
    """
    Check file for clustering

    This function cecks if a file can be accepted for clustering

    Returns:
        cleaned dataframe.
    """
    df_cleaned = dataframe.dropna()
    return df_cleaned

@app.get("/kmeans/status/{task_id}")
async def get_task_status(task_id: str):
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
async def get_task_result(task_id: str):
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
