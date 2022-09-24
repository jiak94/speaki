from typing import Optional

from pydantic import BaseModel

from app.models import Code, Status


class StatusResponse(BaseModel):
    status: Optional[Status]
    code: Code
    msg: Optional[str]
    download_url: Optional[str]
