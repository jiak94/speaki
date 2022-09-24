import json
import logging
from typing import List

from fastapi import HTTPException

from app.database.redis import redis_client
from app.models import BaseModelEncoder
from app.models.voice import VoiceInformation, VoicesResponse
from app.tts.azure import azure_clint
from app.utils import ValueNotExistsError

logger = logging.getLogger(__name__)


def get_voices(service: str, language: str) -> VoicesResponse:
    response = VoicesResponse(voices=[])
    try:
        voices = _get_voices_from_cache(service, language)
        response.voices = voices
    except ValueNotExistsError:
        match service:
            case "azure":
                response.voices = _get_voices_from_azure(language)
            case _:
                raise HTTPException(status_code=400, detail="service not found")

    return response


def _set_languages_to_cache(key: str, voices: List[VoiceInformation]) -> None:
    redis_client.set(key, json.dumps(voices, cls=BaseModelEncoder), 3600)


def _get_voices_from_cache(service: str, language: str) -> List[VoiceInformation]:
    key = _generate_language_key(service, language)
    res = []
    cache = redis_client.get(key)
    if cache is None:
        raise ValueNotExistsError(f"cache not found for {key}")

    voices = json.loads(cache)

    for voice in voices:
        voiceInfo = json.loads(voice)
        res.append(VoiceInformation(**voiceInfo))

    return res


def _generate_language_key(service: str, language: str) -> str:
    return f"{service}:{language}"


def _get_voices_from_azure(language: str) -> List[VoiceInformation]:
    voices = azure_clint.get_voices(language)
    key = _generate_language_key("azure", language)
    try:
        _set_languages_to_cache(key, voices)
    except Exception as e:
        logger.exception(e)

    return voices
