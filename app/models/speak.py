from pydantic import BaseModel

from app.models import Code, Service, Speed


class SpeakRequest(BaseModel):
    service: Service
    text: None | str
    ssml: None | str
    language: str
    callback: None | str
    speed: None | Speed
    voice: str


class SpeakResponse(BaseModel):
    task_id: str
    msg: str
    code: Code
