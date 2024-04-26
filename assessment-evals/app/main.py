from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Container Running": "Assessment Evals", "Port": "8004"}