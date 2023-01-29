from typing import Dict, Optional

from pydantic import AnyUrl, BaseModel

from app.models import Status


class CallbackInfo(BaseModel):
    url: AnyUrl
    headers: Optional[Dict]


class CallbackRequest(BaseModel):
    task_id: str
    status: Status
    msg: str | None
    download_url: str | None
