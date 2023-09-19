from fastapi import FastAPI

# Erstelle eine FastAPI-Instanz
app = FastAPI()

# Definiere eine Route für die Wurzel-URL ("/"), die "Hello, World!" zurückgibt
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
