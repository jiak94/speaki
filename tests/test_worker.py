import os
import uuid

import pytest

from app import config, tasks
from app.controllers.speak import _wrap_with_ssml
from app.models.callback import CallbackInfo
from app.models.record import Record


@pytest.mark.asyncio
async def test_speak(mysql, mock_file, azure):
    config.ENABLE_EXTERNAL_STORAGE = False

    task_id = str(uuid.uuid4())
    Record.create(
        task_id=task_id,
        service="azure",
        status="pending",
        speed="normal",
    )
    ssml = _wrap_with_ssml("Hello World", "medium", "en-US", "en-US-AriaNeural")
    await tasks.speak(ssml, "azure", task_id)
    record = Record.get(task_id=task_id)
    assert record is not None
    assert record.status == "success"
    assert record.download_url is not None

    file_path = os.path.join(config.MEDIA_PATH, os.path.basename(record.download_url))
    assert os.path.exists(file_path)


@pytest.mark.asyncio
async def test_speak_unknown_service(mysql, mock_file, azure):
    task_id = str(uuid.uuid4())
    Record.create(
        task_id=task_id,
        service="azure",
        status="pending",
        speed="normal",
    )
    ssml = _wrap_with_ssml("Hello World", "medium", "en-US", "en-US-AriaNeural")
    await tasks.speak(ssml, "unknown", task_id)
    file_path = os.path.join(config.MEDIA_PATH, f"{task_id}.wav")
    assert not os.path.exists(file_path)

    record = Record.get(task_id=task_id)
    assert record is not None
    assert record.status == "failed"
    assert record.note == "Service not supported"


@pytest.mark.asyncio
async def test_speak_unknow_record(mysql, mock_file, azure):
    ssml = _wrap_with_ssml("Hello World", "medium", "en-US", "en-US-AriaNeural")
    await tasks.speak(ssml, "azure", str(uuid.uuid4()))


def test_storage_service():
    config.EXTERNAL_STORAGE_SERVICE = "azure"
    res = config.get_storage_type()
    assert res == "azure"

    config.EXTERNAL_STORAGE_SERVICE = "s3"
    res = config.get_storage_type()
    assert res == "s3"

    config.EXTERNAL_STORAGE_SERVICE = "something_else"
    res = config.get_storage_type()
    assert res is None

    config.EXTERNAL_STORAGE_SERVICE = ""
    res = tasks.config.get_storage_type()
    assert res is None

    config.EXTERNAL_STORAGE_SERVICE = None
    res = tasks.config.get_storage_type()
    assert res is None


@pytest.mark.asyncio
async def test_callback(httpserver, mysql):
    task_id = str(uuid.uuid4())
    callback_headers = (
        {"Content-Type": "application/json", "Authentication": "Bearer 1234567890"},
    )
    record = Record.create(
        task_id=task_id,
        service="azure",
        status="success",
        callback=CallbackInfo(
            url=httpserver.url_for("/callback"),
            headers=callback_headers,
        ).json(),
        speed="normal",
        download_url="http://localhost:8000/download",
    )

    callback_body = {
        "task_id": record.task_id,
        "status": record.status,
        "download_url": record.download_url,
        "msg": record.note,
    }
    httpserver.expect_request(
        "/callback", method="POST", json=callback_body
    ).respond_with_json({})

    resp = await tasks.callback(record)
    assert resp.status_code == 200
    assert record is not None
    assert record.status == "success"
    assert record.download_url is not None


@pytest.mark.asyncio
async def test_without_callback(mysql):
    task_id = str(uuid.uuid4())
    record = Record.create(
        task_id=task_id,
        service="azure",
        status="success",
        speed="normal",
        download_url="http://localhost:8000/download",
    )

    resp = await tasks.callback(record)
    assert resp is None
