import json
import logging
from typing import List

from fastapi import HTTPException

from app.database import cache
from app.models import BaseModelEncoder
from app.models.voice import VoiceInformation, VoicesResponse
from app.tts.azure import azure_client
from app.utils import ValueNotExistsError


async def get_voices(service: str, language: str) -> VoicesResponse:
    response = VoicesResponse(voices=[])
    try:
        voices = await _get_voices_from_cache(service, language)
        response.voices = voices
    except ValueNotExistsError:
        match service:
            case "azure":
                response.voices = await _get_voices_from_azure(language)
            case _:
                raise HTTPException(status_code=400, detail="service not found")

    return response


async def _set_languages_to_cache(
    service: str, language: str, voices: List[VoiceInformation]
) -> None:
    key = _generate_language_key(service, language)
    await cache.set(key, json.dumps(voices, cls=BaseModelEncoder), ex=3600)


async def _get_voices_from_cache(service: str, language: str) -> List[VoiceInformation]:
    key = _generate_language_key(service, language)
    res = []
    voices_from_cache = await cache.get(key)
    if voices_from_cache is None:
        raise ValueNotExistsError(f"cache not found for {key}")

    voices = json.loads(voices_from_cache)

    for voice in voices:
        voiceInfo = json.loads(voice)
        res.append(VoiceInformation(**voiceInfo))

    return res


def _generate_language_key(service: str, language: str) -> str:
    return f"{service}:{language}"


async def _get_voices_from_azure(language: str) -> List[VoiceInformation]:
    voices = azure_client.get_voices(language)
    try:
        await _set_languages_to_cache("azure", language, voices)
    except Exception as e:
        logging.exception(e)

    return voices
