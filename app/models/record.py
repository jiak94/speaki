from peewee import BlobField, CharField, UUIDField
from playhouse.mysql_ext import JSONField
from app.models import Service, Speed, Status
from app.models.base import BaseModel


class Record(BaseModel):
    task_id = UUIDField(primary_key=True, index=True)
    service = CharField(choices=Service.__members__.keys())
    callback = JSONField(null=True)
    speed = CharField(choices=Speed.__members__.keys(), null=True)
    status = CharField(choices=Status.__members__.keys())
    download_url = CharField(null=True)
    note = CharField(null=True)
    audio_content = BlobField(null=True)
