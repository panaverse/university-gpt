from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Container": "Quiz Management", "Port": "8003"}