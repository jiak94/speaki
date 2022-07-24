from app.models import speak as speak_model
from app.models import record as record_model
from app.models import Code
import uuid
from app import tasks
from app import utils
from app.tts.azure import azure_clint
from app.database.redis import redis_client
from typing import List
import logging
import json

"""
    1. Get the text size, if greater, return error
    2. submit the task to dramatiq
    3. insert into database (id, task_id, service, callback, speed, status, download_url, created_at, updated_at)
"""

logger = logging.getLogger(__name__)


def speak(request: speak_model.SpeakRequest) -> speak_model.SpeakResponse:
    response = speak_model.SpeakResponse(task_id="", msg="", code=Code.OK)
    text = request.text
    text_size = utils.count_text_size(text)

    if text_size > 3000:
        response.code = Code.BAD_REQUEST
        response.msg = "Text size is too large"
        return response

    task_id = str(uuid.uuid4())

    try:
        record_model.Record.create(
            task_id=task_id,
            service=request.service,
            status=record_model.Status.pending,
            callback=request.callback,
            speed=request.speed,
        )
        tasks.speak.send(text, request.service, request.voice, task_id)
        response.task_id = task_id
        response.code = Code.OK
    except Exception as e:
        logger.exception(e)
        response.code = Code.INTERNAL_SERVER_ERROR
        response.msg = "Internal server error"

    return response
