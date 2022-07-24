from app.models import Status, Code
from pydantic import BaseModel
from typing import Optional


class StatusResponse(BaseModel):
    status: Optional[Status]
    code: Code
    msg: Optional[str]
    download_url: Optional[str]
