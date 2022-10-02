import uuid

import fastapi
import pytest

from app.controllers.speak import speak
from app.controllers.status import get_status
from app.controllers.voice import _get_voices_from_cache, _set_languages_to_cache
from app.models.speak import SpeakRequest
from app.models.voice import VoiceInformation


def test_get_status(records):
    for k, v in records.items():
        resp = get_status(v.task_id)
        assert resp.code == 0
        assert resp.status == v.status
        assert resp.msg == ""
        if v.status == "success":
            assert resp.download_url == v.download_url
        else:
            assert resp.download_url is None

    resp = get_status(uuid.uuid4().hex)
    assert resp.code == 404
    assert resp.status == "unknown"


def test_speak_handler(mysql, mocker):
    request = SpeakRequest(
        service="azure",
        text="hello world",
        language="en-US",
        voice="en-US-AriaNeural",
    )
    mock_background_tasks = mocker.patch.object(fastapi.BackgroundTasks, "add_task")
    speak(request, mock_background_tasks)
    mock_background_tasks.add_task.assert_called_once()


@pytest.mark.asyncio
async def test_get_voices_from_redis_hit(docker):
    voices = {
        "zh": [VoiceInformation(name="zh", gender="male")],
        "en": [VoiceInformation(name="en", gender="male")],
    }
    await _set_languages_to_cache("azure", "zh", voices["zh"])
    get = await _get_voices_from_cache("azure", "zh")

    assert get[0].name == "zh"
    assert get[0].gender == "male"
