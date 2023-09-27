"""Module providing Function to run Webserver/API"""
from fastapi import FastAPI, UploadFile
import uvicorn
import pandas as pd

app = FastAPI()

@app.get("/")
def root():
    """
    Handle the root endpoint.

    This function returns a JSON message with a greeting.

    Returns:
        dict: A dictionary containing a greeting message.
    """
    return {"message": "Hello, World!"}


def check_file(dataframef):
    """
    Check file for clustering

    This function cecks if a file can be accepted for clustering

    Returns:
        cleaned dataframe.
    """
    dataframe_cleaned = dataframe.dropna()
    return dataframe_cleaned
    

@app.post("/uploadcsv/")
async def upload_csv(file: UploadFile):
    """
    Uploads a CSV file and returns its contents as a DataFrame.

    Args:
        file (UploadFile): The uploaded CSV file.

    Returns:
        dict: A dictionary containing the DataFrame with the CSV data.
              If the uploaded file is not a CSV, an error message is returned.
    """
    if file.filename.endswith(".csv"):
        # Read the CSV file directly with pandas
        dataframe = pd.read_csv(file.file)
        return {"dataframe": dataframe.to_dict()}
    return {"error": "Die hochgeladene Datei ist keine CSV-Datei."}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
