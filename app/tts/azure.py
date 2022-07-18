from operator import ipow
from app import config
import azure.cognitiveservices.speech as speechsdk


class AzureTTS:
    def __init__(self) -> None:
        AZURE_KEY = config.AZURE_KEY
        AZURE_REGION = config.AZURE_REGION
        AZURE_ENDPOINT = config.AZURE_ENDPOINT

        self.speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_KEY, region=AZURE_REGION
        )
        self.synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )

    def speak(self, text: str, voice: str) -> speechsdk.AudioDataStream:
        self.speech_config.speech_synthesis_voice_name = voice

        result = self.synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return speechsdk.AudioDataStream(result)
        else:
            raise Exception(f"Speech synthesis failed: {result.reason}")


client = AzureTTS()
