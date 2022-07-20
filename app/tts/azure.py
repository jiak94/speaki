from typing import List
import azure.cognitiveservices.speech as speechsdk


class AzureTTS:
    def init(self, key, region) -> None:
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        self.synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )

        self.VOICES = self.synthesizer.get_voices_async().get()

    def speak(self, text: str, voice: str) -> speechsdk.AudioDataStream:
        self.speech_config.speech_synthesis_voice_name = voice

        result = self.synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return speechsdk.AudioDataStream(result)
        else:
            raise Exception(f"Speech synthesis failed: {result.reason}")

    def get_voices(self) -> List:
        if self.VOICES is None:
            self.VOICES = self.synthesizer.get_voices_async().get()
        return self.VOICES


azure_clint = AzureTTS()
