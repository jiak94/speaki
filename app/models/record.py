from peewee import Model, UUIDField, CharField, BlobField
from app.models import Service, Speed, Status
from app.database.database import db


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
        database = db.db
