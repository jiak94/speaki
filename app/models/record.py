from peewee import BlobField, CharField, Model, UUIDField

from app.database.database import db
from app.models import Service, Speed, Status


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
