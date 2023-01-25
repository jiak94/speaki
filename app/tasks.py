import logging
import os
import os.path
import uuid

import azure.cognitiveservices.speech as speechsdk
import httpx
from peewee import DoesNotExist
from tenacity import retry, stop_after_attempt, wait_fixed

from app import config
from app.models import record as record_model
from app.models.callback import CallbackRequest
from app.storage.aws import s3_storage
from app.storage.azure import azure_storage
from app.tts.azure import azure_client

logger = logging.getLogger(__name__)


async def speak(text: str, service: str, task_id: str) -> None:
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
    try:
        await callback(record)
    except httpx.HTTPStatusError:
        logger.info(f"callback failed. destination: {record.callback}")
    except httpx.RequestError as e:
        logger.exception(
            f"callback failed. destination: {record.callback}. reason: {e}"
        )


def _azure_processor(text: str, record: record_model.Record) -> record_model.Record:
    try:
        audio = azure_client.speak(text)
        record.status = record_model.Status.success
        record.download_url = _store_file(audio)

    except Exception as e:
        logger.exception(e)
        record.status = record_model.Status.failed
        record.note = str(e)

    record.save()
    return record


def _store_file(audio: speechsdk.AudioDataStream) -> str:
    audio_id = uuid.uuid4().hex
    file_path = os.path.join(config.MEDIA_PATH, audio_id)
    logger.debug(f"file path: {file_path}")
    audio.save_to_wav_file(file_path)

    match config.get_storage_type():
        case "azure":
            url = azure_storage.upload_file(file_path)
            os.remove(file_path)
        case "s3":
            url = s3_storage.upload_file(file_path)
            os.remove(file_path)
        case _:
            url = _construct_download_url(audio_id)

    return url


def _construct_download_url(id) -> str:
    return f"download/{id}"


@retry(reraise=True, stop=stop_after_attempt(3), wait=wait_fixed(5))
async def callback(record: record_model.Record) -> None | httpx.Response:
    if not record.callback:
        return None
    body = CallbackRequest(
        task_id=str(record.task_id),
        status=record.status,
        download_url=record.download_url,
        msg=record.note,
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(record.callback, json=body.dict())
    response.raise_for_status()
    return response
