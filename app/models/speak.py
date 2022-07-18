from pydantic import BaseModel
import typing
from enum import Enum

from app.models import Code


class Service(str, Enum):
    azure = "azure"


class Speed(str, Enum):
    slow = "slow"
    normal = "normal"
    fast = "fast"


class SpeakRequest(BaseModel):
    service: Service
    text: str
    callback: typing.Optional[str]
    speed: typing.Optional[Speed]
    voice: typing.Optional[str]


class SpeakResponse(BaseModel):
    task_id: str
    msg: str
    code: Code


class DownloadResponse(BaseModel):
    msg: str
    code: Code
    download_url: typing.Optional[str]
