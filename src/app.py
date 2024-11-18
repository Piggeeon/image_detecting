import uvicorn
from fastapi import FastAPI

from src.api.api import tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="127.0.0.1", port=8080)
