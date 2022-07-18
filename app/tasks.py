import dramatiq
from app.tts.azure import client
from azure.cognitiveservices.speech import AudioDataStream
from app.config import REDIS_HOST, REDIS_PORT

from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def speak(text: str, service: str, voice: str, task_id: str) -> None:
    audio = client.speak(text, "en-US-JennyNeural")
    audio.save_to_wav_file("/home/jiakuan/PersonalProject/output.wav")
    audio_data = b""
    audio.read_data(audio_data)


def upload(audio: AudioDataStream) -> None:
    pass
