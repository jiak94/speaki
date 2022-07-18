from app.models import record
from peewee import *
import uuid
import unittest
from app.database.database import db


class DatabaseConnectionTests(unittest.TestCase):
    def setUp(self) -> None:
        db.init("test", host="localhost", port=3306, user="root", password="mysql")
        db.connect()
        db.create_tables([record.Record], safe=True)

    def tearDown(self) -> None:
        try:
            db.drop_tables([record.Record])
        except:
            pass
        db.close()

    def test_check_table(self):
        assert record.Record.table_exists()

    def test_drop_table(self):
        record.Record.drop_table()
        assert not record.Record.table_exists()

    def test_safe(self):
        with self.assertRaises(OperationalError):
            db.create_tables([record.Record], safe=False)


class DatabaseOperationTests(unittest.TestCase):
    def setUp(self) -> None:
        db.init("test", host="localhost", port=3306, user="root", password="mysql")
        db.connect()
        db.create_tables([record.Record], safe=True)
        super().setUp()

    def tearDown(self) -> None:
        try:
            db.drop_tables([record.Record])
        except:
            pass
        db.close()
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
        )

        get = record.Record.get(task_id=task_id)
        assert get.task_id == instance.task_id
        assert get.service == instance.service
        assert get.callback == instance.callback
        assert get.speed == instance.speed
        assert get.status == instance.status
        assert get.download_url == instance.download_url
