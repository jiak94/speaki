import unittest
from fastapi.testclient import TestClient
from app.main import app
import unittest
from app.config import MEDIA_PATH
import os

client = TestClient(app)


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        path = os.path.join(MEDIA_PATH, "test.txt")
        with open(path, "w+") as f:
            f.write("Hello World")

        return super().setUp()

    def test_echo(self):
        response = self.client.get("/echo")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    def test_get_voices(self):
        response = self.client.get("/voices/en")
        assert response.status_code == 200
        assert response.json().get("voices") is not None

    def test_download(self):
        response = self.client.get("/download/test.txt")
        assert response.status_code == 200
        assert response.text == "Hello World"
