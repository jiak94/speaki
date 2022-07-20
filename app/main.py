from fastapi import FastAPI
from app.tts.azure import AzureTTS
from fastapi.staticfiles import StaticFiles
from app import config
from app.models import speak as speak_model
from app.controllers import speak as speak_controller
from app.database.database import db
from app.tts.azure import azure_clint


app = FastAPI()


@app.on_event("startup")
def startup():
    db.init_db()
    azure_clint.init(key=config.AZURE_KEY, region=config.AZURE_REGION)
    app.mount("/media", StaticFiles(directory=config.MEDIA_PATH), name="media")


@app.on_event("shutdown")
def shutdown():
    db.close()


@app.get("/echo")
async def echo():
    return {"msg": "Hello World"}


@app.post("/speak", response_model=speak_model.SpeakResponse)
async def sepak(request: speak_model.SpeakRequest):
    return speak_controller.speak(request)


@app.get("/download/{task_id}", response_model=speak_model.DownloadResponse)
async def download(task_id: str):
    return speak_controller.download(task_id)
