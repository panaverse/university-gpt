import uvicorn

from app.app import create_app
from app.config import settings

app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run("asgi:app", host="0.0.0.0", port=8080, reload=True)
