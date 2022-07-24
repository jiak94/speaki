import dramatiq
from app.config import REDIS_HOST, REDIS_PORT
from app.models import record as record_model
from dramatiq.brokers.redis import RedisBroker
import os.path
from typing import Any, List
from app.config import MEDIA_PATH
from app import config
from app.tts.azure import azure_clint
from app.database.database import db
import logging
import os

logger = logging.getLogger(__name__)

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT)
dramatiq.set_broker(redis_broker)

if os.getenv("WORKER") == "1":
    logger.info("init azuer")
    azure_clint.init(key=config.AZURE_KEY, region=config.AZURE_REGION)
    logger.info("db init")
    db.init_db()


@dramatiq.actor
def speak(text: str, service: str, voice: str, task_id: str) -> None:
    record = record_model.Record.get(task_id=task_id)
    if record is None:
        return

    record.status = record_model.Status.processing
    record.save()

    match service:
        case "azure":
            _azure_processor(text, voice, record)
        case "_":
            record.status = record_model.Status.failed
            record.note = "Service not supported"
            record.save()


def _azure_processor(text: str, voice: str, record: record_model.Record) -> None:
    try:
        file_path = os.path.join(MEDIA_PATH, f"{record.task_id}.wav")
        audio = azure_clint.speak(text, voice)
        audio.save_to_wav_file(file_path)
        logger.info(f"{record.task_id} saved to {file_path}")
        record.status = record_model.Status.success
        record.download_url = file_path
        record.save()
    except Exception as e:
        record.status = record_model.Status.failed
        record.note = str(e)
        record.save()
