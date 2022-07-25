from pydantic import BaseModel
from typing import List


class VoiceInformation(BaseModel):
    name: str
    gender: str


class VoicesResponse(BaseModel):
    voices: List[VoiceInformation]
