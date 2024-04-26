from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Container": "User Management e!!", "Port": "8001"}