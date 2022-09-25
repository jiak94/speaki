import unittest
import uuid
from unittest.mock import MagicMock, patch

from app.controllers.speak import speak
from app.controllers.status import get_status
from app.controllers.voice import _get_voices_from_cache, _set_languages_to_cache
from app.database.database import db
from app.database.redis import redis_client
from app.models import record
from app.models.speak import SpeakRequest
from app.models.voice import VoiceInformation
from app.tts.azure import azure_clint


class TestHandlerSpeak(unittest.TestCase):
    db_data = {}

    def setUp(self) -> None:
        redis_client.init(host="localhost", port=6379)
        db.init_db(
            db_name="test", host="localhost", port=3306, user="root", password="mysql"
        )
        azure_clint.init()

        super().setUp()

        for i in range(30):
            task_id = uuid.uuid4()
            r = record.Record.create(
                task_id=task_id,
                service="azure",
                callback=uuid.uuid4().__str__(),
                speed="normal",
                status="success",
                download_url=uuid.uuid4().__str__(),
                note="",
                audio_content=b"",
            )
            self.db_data[task_id] = r

    def tearDown(self) -> None:
        try:
            db.db.drop_tables([record.Record])
        except:
            pass
        db.close_db()
        super().tearDown()

    def test_get_status(self):
        for k, v in self.db_data.items():
            resp = get_status(v.task_id)
            self.assertEqual(resp.code, 0)
            self.assertEqual(resp.status, "success")
            self.assertEqual(resp.msg, "")
            self.assertEqual(resp.download_url, v.download_url)

    @patch("fastapi.BackgroundTasks")
    def test_speak_handler(self, mock_background_tasks: MagicMock):
        request = SpeakRequest(
            service="azure",
            text="hello world",
            language="en-US",
            voice="en-US-AriaNeural",
        )
        with patch.object(mock_background_tasks, "add_task") as mock_add_task:
            speak(request, mock_background_tasks)
            mock_add_task.assert_called_once()

    def test_get_voices_from_redis_hit(self):
        voices = {
            "zh": [VoiceInformation(name="zh", gender="male")],
            "en": [VoiceInformation(name="en", gender="male")],
        }
        _set_languages_to_cache("azure", "zh", voices["zh"])
        get = _get_voices_from_cache("azure", "zh")

        assert get[0].name == "zh"
        assert get[0].gender == "male"
