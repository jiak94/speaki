from pydantic import BaseModel

from app.models import Code, Service, Speed
from app.models.callback import CallbackInfo

class SpeakRequest(BaseModel):
    service: Service
    text: None | str
    ssml: None | str
    language: str
    callback: None | CallbackInfo
    speed: None | Speed
    voice: str


class SpeakResponse(BaseModel):
    task_id: str
    msg: str
    code: Code
