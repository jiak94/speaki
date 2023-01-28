import logging
import uuid

from fastapi import BackgroundTasks

from app import tasks
from app.models import Code, record as record_model, speak as speak_model

"""
    1. Get the text size, if greater, return error
    2. submit the task to background
    3. insert into database (id, task_id, service, callback, speed, status, download_url, created_at, updated_at)
"""

logger = logging.getLogger(__name__)


def speak(
    request: speak_model.SpeakRequest, background_tasks: BackgroundTasks
) -> speak_model.SpeakResponse:
    response = speak_model.SpeakResponse(task_id="", msg="", code=Code.OK)
    text = request.text

    task_id = str(uuid.uuid4())

    try:
        record: record_model.Record = record_model.Record.create(
            task_id=task_id,
            service=request.service,
            status=record_model.Status.pending,
            callback=request.callback.dict() if request.callback else None,
            speed=request.speed if request.speed else record_model.Speed.normal,
        )
        if request.text:
            ssml = _wrap_with_ssml(text, record.speed, request.language, request.voice)
        else:
            ssml = request.ssml
        logger.debug(f"ssml: {ssml}")
        background_tasks.add_task(tasks.speak, ssml, request.service, task_id)
        response.task_id = task_id
        response.code = Code.OK
    except Exception as e:
        logger.exception(e)
        response.code = Code.INTERNAL_SERVER_ERROR
        response.msg = "cannot process request at this moment"

    return response


def _wrap_with_ssml(text: str, speed: str, language: str, voice: str) -> str:
    return f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{language}'><voice name='{voice}'><prosody rate='{speed}'>{text}</prosody></voice></speak>"
