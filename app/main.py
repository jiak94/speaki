import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app import config
from app.models.speak import SpeakRequest, SpeakResponse
from app.models.voice import VoicesResponse
from app.models.status import StatusResponse
from app.controllers import speak as speak_controller
from app.controllers import voice as voice_controller
from app.controllers import status as status_controller
from app.database.database import db
from app.database.redis import redis_client
from app.tts.azure import azure_clint
from app.storage.azure import azure_storage
import os


app = FastAPI()
logger = logging.getLogger(__name__)


@app.on_event("startup")
def startup():
    db.init_db()
    logger.error(f"azure_key:{config.AZURE_KEY}")
    azure_clint.init(key=config.AZURE_KEY, region=config.AZURE_REGION)
    redis_client.init()
    azure_storage.init()


@app.on_event("shutdown")
def shutdown():
    db.close_db()


@app.get("/echo")
async def echo():
    return {"msg": "Hello World"}


@app.post("/speak", response_model=SpeakResponse)
async def speak(request: SpeakRequest):
    return speak_controller.speak(request)


@app.get("/status/{task_id}", response_model=StatusResponse)
async def get_status(task_id: str):
    return status_controller.get_status(task_id)


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_location = os.path.join(config.MEDIA_PATH, file_name)
    return FileResponse(
        file_location, media_type="application/octet-stream", filename=file_name
    )


@app.get("/voices/{lang}", response_model=VoicesResponse)
async def get_voices(lang: str):
    return voice_controller.get_voices(lang)
