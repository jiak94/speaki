from pydantic import BaseModel

from app.models import Status


class CallbackRequest(BaseModel):
    task_id: str
    status: Status
    msg: str | None
    download_url: str | None
