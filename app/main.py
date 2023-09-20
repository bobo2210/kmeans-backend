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
        # CSV-Datei direkt mit pandas einlesen
        df = pd.read_csv(file.file)
    
        return {"dataframe": df}
    else:
        return {"error": "Die hochgeladene Datei ist keine CSV-Datei."}

if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
