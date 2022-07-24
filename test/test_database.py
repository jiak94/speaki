import time
from app.models import record
from peewee import *
import uuid
import unittest
from app.database.database import db
from app.database.redis import redis_client
from app.models import BaseModelEncoder


class DatabaseConnectionTests(unittest.TestCase):
    def setUp(self) -> None:
        db.init_db(
            db_name="test", host="localhost", port=3306, user="root", password="mysql"
        )
        super().setUp()

    def tearDown(self) -> None:
        try:
            db.db.drop_tables([record.Record])
        except:
            pass
        db.close_db()
        super().tearDown()

    def test_check_table(self):
        assert record.Record.table_exists()

    def test_drop_table(self):
        record.Record.drop_table()
        assert not record.Record.table_exists()

    def test_safe(self):
        with self.assertRaises(OperationalError):
            db.db.create_tables([record.Record], safe=False)


class DatabaseOperationTests(unittest.TestCase):
    def setUp(self) -> None:
        db.init_db(
            db_name="test", host="localhost", port=3306, user="root", password="mysql"
        )
        super().setUp()

    def tearDown(self) -> None:
        try:
            db.db.drop_tables([record.Record])
        except:
            pass
        db.close_db()
        super().tearDown()

    def test_record_write(self):
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


class RedisOperationTests(unittest.TestCase):
    def setUp(self) -> None:
        redis_client.init(host="localhost", port=6379)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_set_redis(self):
        key = "test-key"
        value = "test-value"

        redis_client.set(key, value.encode("utf-8"))

        get = redis_client.get(key).decode("utf-8")

        assert get == value

    def test_set_expiration(self):
        key = "test-exp-key"
        value = "test-exp-value"

        redis_client.set(key, value.encode("utf-8"), expiration=1)

        time.sleep(3)

        get = redis_client.get(key)

        assert get == None
