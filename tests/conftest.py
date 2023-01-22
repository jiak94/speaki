import asyncio
import os
import shutil
import uuid

import pytest
from peewee import MySQLDatabase

from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_S3_CONTAINER_NAME,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    AZURE_BLOB_CONNECTION_STRING,
    MEDIA_PATH,
)
from app.database.database import db
from app.models import record
from app.storage.aws import aws_storage
from app.storage.azure import azure_storage
from app.tts.azure import azure_clint


@pytest.fixture(scope="session")
def docker_compose_command():
    return "docker compose"


@pytest.fixture(scope="session")
def docker(docker_services):
    def test_mysql():
        try:
            mysql_db = MySQLDatabase(None)
            mysql_db.init(
                'test', user='root', password='mysql', host="localhost", port=3306
            )
            mysql_db.connect()
            return mysql_db.is_connection_usable()
        except:
            return False

    docker_services.wait_until_responsive(timeout=60, pause=1, check=test_mysql)

    docker_services.wait_until_responsive(
        timeout=60,
        pause=1,
        check=lambda: docker_services.port_for("redis", 6379) is not None,
    )


@pytest.fixture(scope="session")
def mysql(docker):
    db.connect()
    db.create_tables([record.Record])
    db.close()


@pytest.fixture
def records(mysql):
    records = {}
    for i in range(30):
        task_id = uuid.uuid4()
        if i % 4 == 0:
            status = "pending"
        elif i % 4 == 1:
            status = "processing"
        elif i % 4 == 2:
            status = "success"
        else:
            status = "failed"
        r = record.Record.create(
            task_id=task_id,
            service="azure",
            callback=uuid.uuid4().__str__(),
            speed="normal",
            status=status,
            download_url=uuid.uuid4().__str__(),
            note="",
            audio_content=b"",
        )
        records[task_id] = r
    return records


@pytest.fixture(scope="session")
def azure():
    azure_clint.init()


@pytest.fixture
def mock_file():
    os.path.exists(MEDIA_PATH) or os.mkdir(MEDIA_PATH)
    path = os.path.join(MEDIA_PATH, "test.txt")
    with open(path, "w+") as f:
        f.write("Hello World")


@pytest.fixture(scope="session")
def azure_storage_service():
    azure_storage.init(AZURE_BLOB_CONNECTION_STRING, "test1")
    return azure_storage


@pytest.fixture(scope="session")
def aws_storage_service():
    print(f"key: {AWS_ACCESS_KEY_ID}")
    aws_storage.init(
        "",
        "",
        "us-west-1",
        "speaki.test.bucket",
    )
    return aws_storage


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


def pytest_sessionfinish(session, exitstatus):
    try:
        shutil.rmtree(MEDIA_PATH)
    except:
        pass
