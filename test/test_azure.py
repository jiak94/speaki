import unittest
from app.tts.azure import AzureTTS


class TestTTS(unittest.TestCase):
    def setUp(self) -> None:
        self.azure = AzureTTS()
        self.azure.init()
        super().setUp()

    def test_azure_without_voice(self):
        try:
            self.azure.speak("Hello World")
        except Exception as e:
            print(e)
            assert False

    def test_azure_with_voice(self):
        try:
            self.azure.speak("Hello World", "en-US-AriaNeural")
        except Exception as e:
            print(e)
            assert False

    def test_azure_get_voices(self):
        voices = self.azure.get_voices()
        assert len(voices) > 0
