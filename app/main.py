"""Module providing Function to run Webserver/API"""
from fastapi import FastAPI, UploadFile
import uvicorn
import pandas as pd  # Import pandas module

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

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
