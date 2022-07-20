import unittest
from app.controllers.speak import download
from app.database.database import db
from app.models import record


class TestHandlerSpeak(unittest.TestCase):
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

    def test_handler_download(self):
        pass
