import logging
import os

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse

from app import config
from app.controllers import (
    speak as speak_controller,
    status as status_controller,
    voice as voice_controller,
)
from app.database.database import db
from app.database.redis import redis_client
from app.models.speak import SpeakRequest, SpeakResponse
from app.models.status import StatusResponse
from app.models.voice import VoicesResponse
from app.storage.azure import azure_storage
from app.tts.azure import azure_clint

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
async def speak(request: SpeakRequest, background_tasks: BackgroundTasks):
    if request.text and request.ssml:
        raise HTTPException(status_code=400, detail="chose either text or ssml")

    return speak_controller.speak(request, background_tasks)


@app.get("/status/{task_id}", response_model=StatusResponse)
async def get_status(task_id: str):
    return status_controller.get_status(task_id)


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_location = os.path.join(config.MEDIA_PATH, file_name)
    return FileResponse(
        file_location, media_type="application/octet-stream", filename=file_name
    )


@app.get("/voices/", response_model=VoicesResponse)
async def get_voices(service: str | None = None, language: str | None = None):
    if not service or not language:
        raise HTTPException(status_code=400, detail="service and language are required")

    return voice_controller.get_voices(service, language)
