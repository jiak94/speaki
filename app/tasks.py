import dramatiq
from app.config import REDIS_HOST, REDIS_PORT
from app.models import record as record_model
from dramatiq.brokers.redis import RedisBroker
import os.path
from app import config
from app.tts.azure import azure_clint
from app.database.database import db
import logging
import os
from peewee import DoesNotExist
from app.storage.azure import azure_storage
import uuid


logger = logging.getLogger(__name__)

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT)
dramatiq.set_broker(redis_broker)

if config.WORKER_MODE:
    logger.info("init azuer")
    azure_clint.init(key=config.AZURE_KEY, region=config.AZURE_REGION)
    logger.info("db init")
    db.init_db()
    azure_storage.init()


@dramatiq.actor
def speak(text: str, service: str, voice: str, task_id: str) -> None:
    try:
        record = record_model.Record.get(task_id=task_id)
    except DoesNotExist:
        logger.info(f"record {task_id} not found")
        return

    record.status = record_model.Status.processing
    record.save()

    match service:
        case "azure":
            _azure_processor(text, voice, record)
        case _:
            record.status = record_model.Status.failed
            record.note = "Service not supported"
            record.save()
            print("Service not supported saved!")


def _azure_processor(text: str, voice: str, record: record_model.Record) -> None:
    try:
        audio = azure_clint.speak(text, voice)
        record.status = record_model.Status.success
        record.download_url = _store_file(audio)
        record.save()
    except Exception as e:
        record.status = record_model.Status.failed
        record.note = str(e)
        record.save()


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
