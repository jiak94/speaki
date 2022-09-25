import os
import shutil
import unittest
import uuid

import pytest

from app import config, tasks
from app.controllers.speak import _wrap_with_ssml
from app.database.database import db
from app.database.redis import redis_client
from app.models.record import Record
from app.tts.azure import azure_clint


@pytest.mark.usefixtures("docker")
class TestWorker(unittest.TestCase):
    def setUp(self) -> None:
        os.path.exists(config.MEDIA_PATH) or os.mkdir(config.MEDIA_PATH)
        redis_client.init(host="localhost", port=6379)
        db.init_db(
            db_name="test", host="localhost", port=3306, user="root", password="mysql"
        )
        azure_clint.init()
        self.ssml = _wrap_with_ssml(
            "Hello World", "medium", "en-US", "en-US-AriaNeural"
        )
        config.ENABLE_EXTERNAL_STORAGE = False
        super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(config.MEDIA_PATH)
        return super().tearDown()

    def test_speak(self):
        task_id = str(uuid.uuid4())
        Record.create(
            task_id=task_id,
            service="azure",
            status="pending",
            callback="http://localhost:8000/callback",
            speed="normal",
        )

        tasks.speak(self.ssml, "azure", task_id)
        record = Record.get(task_id=task_id)
        assert record is not None
        assert record.status == "success"
        assert record.download_url is not None

        file_path = os.path.join(
            config.MEDIA_PATH, os.path.basename(record.download_url)
        )
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
        tasks.speak(self.ssml, "unknown", task_id)
        file_path = os.path.join(config.MEDIA_PATH, f"{task_id}.wav")
        assert not os.path.exists(file_path)

        record = Record.get(task_id=task_id)
        assert record is not None
        assert record.status == "failed"
        assert record.note == "Service not supported"

    def test_speak_unknow_record(self):
        try:
            tasks.speak(self.ssml, "azure", str(uuid.uuid4()))
        except Exception:
            assert False

    def test_storage_service(self):
        config.ENABLE_EXTERNAL_STORAGE = True
        config.EXTERNAL_STORAGE_SERVICE = "azure"
        res = tasks._enable_cloud_storage()
        assert res is True

        config.EXTERNAL_STORAGE_SERVICE = ""
        res = tasks._enable_cloud_storage()
        assert res is True

        config.EXTERNAL_STORAGE_SERVICE = None
        res = tasks._enable_cloud_storage()
        assert res is False

        config.ENABLE_EXTERNAL_STORAGE = False
        res = tasks._enable_cloud_storage()
        assert res is False
