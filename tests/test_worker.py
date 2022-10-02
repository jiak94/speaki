import os
import uuid

import pytest

from app import config, tasks
from app.controllers.speak import _wrap_with_ssml
from app.models.record import Record


@pytest.mark.asyncio
async def test_speak(mysql, mock_file, azure):
    config.ENABLE_EXTERNAL_STORAGE = False

    task_id = str(uuid.uuid4())
    Record.create(
        task_id=task_id,
        service="azure",
        status="pending",
        callback="http://localhost:8000/callback",
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
        callback="http://localhost:8000/callback",
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


@pytest.mark.asyncio
def test_storage_service():
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


@pytest.mark.asyncio
async def test_callback(httpserver, mysql):
    task_id = str(uuid.uuid4())
    record = Record.create(
        task_id=task_id,
        service="azure",
        status="success",
        callback=httpserver.url_for("/callback"),
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
