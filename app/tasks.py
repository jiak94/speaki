import logging
import os
import os.path
import uuid

import requests
from peewee import DoesNotExist
from tenacity import retry, stop_after_attempt, wait_fixed

from app import config
from app.models import record as record_model
from app.models.callback import CallbackRequest
from app.storage.azure import azure_storage
from app.tts.azure import azure_clint

logger = logging.getLogger(__name__)


def speak(text: str, service: str, task_id: str) -> None:
    try:
        record = record_model.Record.get(task_id=task_id)
    except DoesNotExist:
        logger.info(f"record {task_id} not found")
        return

    record.status = record_model.Status.processing
    record.save()

    match service:
        case "azure":
            record = _azure_processor(text, record)
        case _:
            record.status = record_model.Status.failed
            record.note = "Service not supported"
            record.save()
            logger.info("service not supported")

    if record.callback is not None:
        body = CallbackRequest(
            task_id=record.task_id,
            status=record.status,
            download_url=record.download_url,
        )
        _callback(record.callback, body)


def _azure_processor(text: str, record: record_model.Record) -> record_model.Record:
    try:
        audio = azure_clint.speak(text)
        record.status = record_model.Status.success
        record.download_url = _store_file(audio)

    except Exception as e:
        record.status = record_model.Status.failed
        record.note = str(e)

    record.save()
    return record


def _store_file(audio) -> str:
    audio_id = uuid.uuid4().hex
    file_path = os.path.join(config.MEDIA_PATH, audio_id)
    audio.save_to_wav_file(file_path)
    if _enable_cloud_storage():
        try:
            match config.EXTERNAL_STORAGE_SERVICE:
                case "azure":
                    url = azure_storage.upload_file(file_path)
                case _:
                    url = _construct_download_url(audio_id)

            os.remove(file_path)
            return url
        except Exception as e:
            logger.exception(e)
            return _construct_download_url(audio_id)
    else:
        return _construct_download_url(audio_id)


def _construct_download_url(id) -> str:
    return f"download/{id}"


def _enable_cloud_storage() -> bool:
    return (
        config.ENABLE_EXTERNAL_STORAGE and config.EXTERNAL_STORAGE_SERVICE is not None
    )


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def _callback(url: str, callback_body: CallbackRequest) -> None:
    response = requests.post(url, json=callback_body.dict())
    response.raise_for_status()
