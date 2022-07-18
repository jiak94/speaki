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


class Status(str, Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"


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
    status: Status
    msg: typing.Optional[str]
    download_url: typing.Optional[str]
