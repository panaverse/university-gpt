from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Container": "Question Bank Running", "Port": "8002"}