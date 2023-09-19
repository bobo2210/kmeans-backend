from fastapi import FastAPI

# Erstelle eine FastAPI-Instanz
app = FastAPI()

# Definiere eine Route für die Wurzel-URL ("/"), die "Hello, World!" zurückgibt
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
