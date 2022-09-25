from typing import List

from pydantic import BaseModel


class VoiceInformation(BaseModel):
    name: str
    gender: str


class VoicesResponse(BaseModel):
    voices: List[VoiceInformation]
