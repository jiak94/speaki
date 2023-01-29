from peewee import BlobField, CharField, TextField, UUIDField

from app.models import Service, Speed, Status
from app.models.base import BaseModel


class Record(BaseModel):
    task_id = UUIDField(primary_key=True, index=True)
    service = CharField(choices=Service.__members__.keys())
    callback = TextField(null=True)
    speed = CharField(choices=Speed.__members__.keys(), null=True)
    status = CharField(choices=Status.__members__.keys())
    download_url = TextField(null=True)
    note = TextField(null=True)
    audio_content = BlobField(null=True)
