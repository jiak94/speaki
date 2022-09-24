import os
import unittest

from fastapi.testclient import TestClient

from app.config import MEDIA_PATH
from app.database.redis import redis_client
from app.main import app
from app.tts.azure import azure_clint

client = TestClient(app)


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        azure_clint.init()
        redis_client.init(host="localhost", port=6379)
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
        response = self.client.get(
            "/voices", params={"service": "azure", "language": "en-US"}
        )
        assert response.status_code == 200
        assert response.json().get("voices") is not None

    def test_download(self):
        response = self.client.get("/download/test.txt")
        assert response.status_code == 200
        assert response.text == "Hello World"

    def test_speak_invalid(self):
        response = self.client.post("/speak", json={"text": "Hello World"})
        assert response.status_code == 422

        response = self.client.post("/speak", json={"ssml": "Hello World"})
        assert response.status_code == 422

        body = {
            "text": "Hello World",
            "ssml": "Hello World",
            "voice": "en-US-AriaNeural",
            "speed": "medium",
            "service": "azure",
            "language": "en-US",
        }
        response = self.client.post("/speak", json=body)
        assert response.status_code == 400
