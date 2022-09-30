from peewee import Model

from app.database.database import db


class BaseModel(Model):
    class Meta:
        database = db.db
