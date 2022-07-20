from pydantic import BaseModel
import typing

from app.models import Code, Service, Speed, Status


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
    status: typing.Optional[Status]
    code: Code
    msg: typing.Optional[str]
    download_url: typing.Optional[str]
