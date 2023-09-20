"""Module providing Function to run Webserver/API"""
from fastapi import FastAPI
import uvicorn

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

if __name__=='__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
