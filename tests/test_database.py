import uuid

import pytest

from app.database import cache
from app.models import record


def test_record_write(mysql):
    task_id = uuid.uuid4()
    instance = record.Record.create(
        task_id=task_id,
        service="azure",
        callback="http://localhost:8000/callback",
        speed="normal",
        status="pending",
        download_url=f"http://localhost:8000/download/{task_id}",
        note="test",
        audio_content=b"test",
    )

    get = record.Record.get(task_id=task_id)
    assert get.task_id == instance.task_id
    assert get.service == instance.service
    assert get.callback == instance.callback
    assert get.speed == instance.speed
    assert get.status == instance.status
    assert get.download_url == instance.download_url


@pytest.mark.asyncio
async def test_set_redis(redis):
    key = "test-key"
    value = "test-value"

    await cache.set(key, value.encode("utf-8"))

    get = (await cache.get(key)).decode("utf-8")

    assert get == value
