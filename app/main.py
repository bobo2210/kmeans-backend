"""Module providing Function to run Webserver/API"""
from fastapi import FastAPI
from uvicorn import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__=='__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
