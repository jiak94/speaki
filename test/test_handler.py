import unittest
from app.controllers.status import get_status
from app.controllers.voice import (
    _set_languages_to_cache,
    _get_voices_from_cache,
    _split_voice_by_language,
)
from app.database.database import db
from app.database.redis import redis_client
from app.tts.azure import azure_clint
from app.models import record
import uuid

from app.models.voice import VoiceInformation


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

    def test_speak_handler(self):
        pass

    def test_get_voices_from_redis_hit(self):
        voices = {
            "zh": [VoiceInformation(name="zh", gender="male")],
            "en": [VoiceInformation(name="en", gender="male")],
        }

        _set_languages_to_cache(voices)
        get = _get_voices_from_cache("zh")

        assert get[0].name == "zh"
        assert get[0].gender == "male"

    def test_split_voice_by_language(self):
        languages = [
            VoiceInformation(name="zh-test1", gender="male"),
            VoiceInformation(name="zh-test2", gender="male"),
            VoiceInformation(name="zh-test3", gender="male"),
            VoiceInformation(name="en-test1", gender="male"),
            VoiceInformation(name="en-test1", gender="male"),
            VoiceInformation(name="es-test1", gender="male"),
            VoiceInformation(name="es-test1", gender="male"),
            VoiceInformation(name="es-test1", gender="male"),
            VoiceInformation(name="es-test1", gender="male"),
        ]
        get = _split_voice_by_language(languages)

        assert len(get) == 3
        assert len(get["zh"]) == 3
        assert len(get["en"]) == 2
        assert len(get["es"]) == 4
