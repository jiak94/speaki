import azure.cognitiveservices.speech as speechsdk

from app import config
from app.models.voice import VoiceInformation


class AzureTTS:
    inited = False

    def init(self, key=config.AZURE_SPEECH_KEY, region=config.AZURE_SPEECH_REGION) -> None:
        print(f"init azure tts client, key: {config.AZURE_SPEECH_KEY}, region: {config.AZURE_SPEECH_REGION}")

        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        self.inited = True

    def speak(self, text: str) -> speechsdk.AudioDataStream:
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )
        result = synthesizer.speak_ssml_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return speechsdk.AudioDataStream(result)
        else:
            cancellation_details = result.cancellation_details
            raise Exception(f"Speech synthesis failed: {cancellation_details}")

    def get_voices(self, language: str) -> list:
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )

        result: speechsdk.SynthesisVoicesResult = synthesizer.get_voices_async(
            language
        ).get()
        res = []
        for voice in result.voices:
            gender = ""
            match voice.gender:
                case speechsdk.SynthesisVoiceGender.Male:
                    gender = "male"
                case speechsdk.SynthesisVoiceGender.Female:
                    gender = "female"
                case _:
                    gender = "unknown"

            voiceInfo = VoiceInformation(name=voice.short_name, gender=gender)
            res.append(voiceInfo)

        return res


azure_client = AzureTTS()
