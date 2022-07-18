from enum import Enum
from peewee import Model, UUIDField, CharField, BlobField
import datetime
from app.database.database import db


class Service(Enum):
    azure = "azure"
    aws = "aws"


class Status(Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"


class Speed(Enum):
    slow = "slow"
    normal = "normal"
    fast = "fast"


class Record(Model):
    task_id = UUIDField(primary_key=True, index=True)
    service = CharField(choices=Service.__members__.keys())
    callback = CharField(null=True)
    speed = CharField(choices=Speed.__members__.keys(), null=True)
    status = CharField(choices=Status.__members__.keys())
    download_url = CharField(null=True)
    note = CharField(null=True)
    audio_content = BlobField(null=True)

    class Meta:
        database = db
