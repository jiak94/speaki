from fastapi import FastAPI
from app.models import speak
from app.database import database

app = FastAPI()


@app.on_event("startup")
def startup():
    database.init_db()


@app.on_event("shutdown")
def shutdown():
    database.close()


@app.get("/echo")
async def echo():
    return {"msg": "Hello World"}


@app.post("/speech")
async def speech(request: speak.SpeakRequest, response: speak.SpeakResponse):
    pass


@app.get("/download/{task_id}")
async def download(task_id: str, response: speak.DownloadResponse):
    pass
