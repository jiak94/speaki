import unittest
from fastapi.testclient import TestClient
from app.main import app
import unittest

client = TestClient(app)


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        return super().setUp()

    def test_echo(self):
        response = self.client.get("/echo")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    def test_get_voices(self):
        response = self.client.get("/voices/en")
        assert response.status_code == 200
        assert response.json().get("voices") is not None
