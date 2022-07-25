import unittest
from app.database.database import db
from app.database.redis import redis_client
from app.tts.azure import azure_clint
from app import tasks
import uuid
import os
from app.models.record import Record
from app import config


class TestWorker(unittest.TestCase):
    def setUp(self) -> None:
        redis_client.init(host="localhost", port=6379)
        db.init_db(
            db_name="test", host="localhost", port=3306, user="root", password="mysql"
        )
        azure_clint.init()

        super().setUp()

    def test_speak(self):
        task_id = str(uuid.uuid4())
        Record.create(
            task_id=task_id,
            service="azure",
            status="pending",
            callback="http://localhost:8000/callback",
            speed="normal",
        )

        tasks.speak("Hello World", "azure", "en-US-AriaNeural", task_id)
        record = Record.get(task_id=task_id)
        assert record is not None
        assert record.status == "success"
        assert record.download_url is not None

        file_path = os.path.join(config.MEDIA_PATH, f"{task_id}.wav")
        assert os.path.exists(file_path)

    def test_speak_unknown_service(self):
        task_id = str(uuid.uuid4())
        Record.create(
            task_id=task_id,
            service="azure",
            status="pending",
            callback="http://localhost:8000/callback",
            speed="normal",
        )
        tasks.speak("Hello World", "unknown", "en-US-AriaNeural", task_id)
        file_path = os.path.join(config.MEDIA_PATH, f"{task_id}.wav")
        assert not os.path.exists(file_path)

        record = Record.get(task_id=task_id)
        assert record is not None
        assert record.status == "failed"
        assert record.note == "Service not supported"

    def test_speak_unknow_record(self):
        try:
            tasks.speak("Hello World", "azure", "en-US-AriaNeural", str(uuid.uuid4()))
        except Exception as e:
            assert False
