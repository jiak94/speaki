from pydantic import BaseModel
import typing

from app.models import Code, Service, Speed


class SpeakRequest(BaseModel):
    service: Service
    text: str
    callback: typing.Optional[str]
    speed: typing.Optional[Speed]
    voice: str


class SpeakResponse(BaseModel):
    task_id: str
    msg: str
    code: Code
