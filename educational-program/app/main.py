from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Container 1": "Educational Program!!!", "Port": "8000"}