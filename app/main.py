import logging
import os

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse

import app.utils as utils
from app import config
from app.controllers import (
    speak as speak_controller,
    status as status_controller,
    voice as voice_controller,
)
from app.database.database import db, db_state_default
from app.models.record import Record
from app.models.speak import SpeakRequest, SpeakResponse
from app.models.status import StatusResponse
from app.models.voice import VoicesResponse
from app.storage.azure import azure_storage
from app.tts.azure import azure_clint

app = FastAPI()
logger = logging.getLogger(__name__)


@app.on_event("startup")
def startup():
    db.connect()
    db.create_tables([Record])
    db.close()
    logger.error(f"azure_key:{config.AZURE_KEY}")
    azure_clint.init(key=config.AZURE_KEY, region=config.AZURE_REGION)
    azure_storage.init()


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


@app.get("/echo")
async def echo():
    return {"msg": "Hello World"}


@app.post("/speak", response_model=SpeakResponse, dependencies=[Depends(get_db)])
async def speak(request: SpeakRequest, background_tasks: BackgroundTasks):
    if request.text and request.ssml:
        raise HTTPException(status_code=400, detail="chose either text or ssml")
    if request.text and utils.count_text_size(request.text) > 3000:
        raise HTTPException(status_code=400, detail="text is too long")

    return speak_controller.speak(request, background_tasks)


@app.get(
    "/status/{task_id}", response_model=StatusResponse, dependencies=[Depends(get_db)]
)
async def get_status(task_id: str):
    return status_controller.get_status(task_id)


@app.get("/download/{file_name}", dependencies=[Depends(get_db)])
async def download_file(file_name: str):
    file_location = os.path.join(config.MEDIA_PATH, file_name)
    return FileResponse(
        file_location, media_type="application/octet-stream", filename=file_name
    )


@app.get("/voices", response_model=VoicesResponse)
async def get_voices(service: str | None = None, language: str | None = None):
    if not service or not language:
        raise HTTPException(status_code=400, detail="service and language are required")

    return await voice_controller.get_voices(service, language)
