from app.models import BaseModelEncoder
from app.models.voice import VoicesResponse, VoiceInformation
from app.database.redis import redis_client
from app.tts.azure import azure_clint
import json
from typing import List


def get_voices(lang: str) -> VoicesResponse:
    response = VoicesResponse(voices=[])
    voices = _get_voices_from_cache(lang)
    if len(voices) == 0:
        voices = azure_clint.get_voices()
        languages = _split_voice_by_language(voices)
        response.voices = languages.get(lang, [])
    else:
        response.voices = voices
    return response


def _split_voice_by_language(
    voices: List[VoiceInformation],
) -> dict[str, List[VoiceInformation]]:
    languages = {}
    for voice in voices:
        name = voice.name
        lang = name.split("-")[0]
        if lang not in languages:
            languages[lang] = []
        languages[lang].append(voice)
    _set_languages_to_cache(languages)
    return languages


def _set_languages_to_cache(languages: dict[str, List[VoiceInformation]]) -> None:
    for lang, voices in languages.items():
        redis_client.set(lang, json.dumps(voices, cls=BaseModelEncoder), 3600)


def _get_voices_from_cache(language: str) -> List[VoiceInformation]:
    res = []
    cache = redis_client.get(language)
    if cache is None:
        return res

    voices = json.loads(cache)

    if voices is None:
        return res

    for voice in voices:
        voiceInfo = json.loads(voice)
        res.append(VoiceInformation(**voiceInfo))

    return res
