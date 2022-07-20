from app.models import speak as speak_model
from app.models import record as record_model
from app.models import Code, Status, Service
import uuid
from app import tasks
import langdetect
from app import utils
from app.tts.azure import azure_clint
from typing import Optional
from peewee import DoesNotExist

"""
    1. Get the text size, if greater, return error
    2. submit the task to dramatiq
    3. insert into database (id, task_id, service, callback, speed, status, download_url, created_at, updated_at)
"""


def speak(request: speak_model.SpeakRequest) -> speak_model.SpeakResponse:
    response = speak_model.SpeakResponse(task_id="", msg="", code=Code.OK)
    text = request.text
    text_size = utils.count_text_size(text)

    if text_size > 3000:
        response.code = Code.BAD_REQUEST
        response.msg = "Text size is too large"
        return response

    task_id = uuid.uuid4()
    response.task_id = task_id
    voice = request.voice or _get_default_voice(request, _detect_language(text))
    try:
        record_model.Record(
            task_id=task_id,
            service=request.service,
            status=record_model.Status.pending,
            callback=request.callback,
            speed=request.speed,
        ).create()
        tasks.speak.send(text, request.service, voice, task_id)
        response.code = Code.OK
    except Exception:
        response.code = Code.INTERNAL_SERVER_ERROR
        response.msg = "Internal server error"

    return response


def _detect_language(text: str) -> str:
    return langdetect.detect(text)


def _get_default_voice(
    request: speak_model.SpeakRequest, language: str
) -> Optional[str]:
    match request.service:
        case Service.azure:
            return _get_azure_default_voice(language)
        case _:
            return None


def _get_azure_default_voice(language: str) -> Optional[str]:
    language_list = azure_clint.get_voices(language)
    for lang in language_list:
        if language in lang["Locale"]:
            return lang["ShortName"]
    return None


def download(task_id: str) -> speak_model.DownloadResponse:
    response = speak_model.DownloadResponse(code=Code.OK)

    try:
        record = record_model.Record.get(task_id=task_id)
        response.status = Code.OK
        match record.status:
            case Status.success:
                response.msg = "Success"
                response.download_url = record.download_url
                return response
            case Status.failed:
                response.msg = record.note
                return response
            case Status.processing:
                return response
            case Status.pending:
                return response
            case _:
                response.status = Code.BAD_REQUEST
                response.msg = "Unknown status"
                return response
    except DoesNotExist:
        response.code = Code.NOT_FOUND
        response.msg = "Record Not found"
        return response
    except:
        response.code = Code.INTERNAL_SERVER_ERROR
        response.msg = "Internal server error"
        return response
