import unittest

from app.controllers.speak import _wrap_with_ssml
from app.tts.azure import AzureTTS


class TestTTS(unittest.TestCase):
    def setUp(self) -> None:
        self.azure = AzureTTS()
        self.azure.init()
        super().setUp()

    def test_azure_without_voice(self):
        ssml = _wrap_with_ssml("Hello World", "medium", "en-US", "en-US-AriaNeural")

        try:
            self.azure.speak(ssml)
        except Exception as e:
            print(e)
            assert False


def test_azure_get_voices(azure):
    voices = azure.get_voices("en-US")
    assert len(voices) > 0
