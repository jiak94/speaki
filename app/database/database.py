from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from app.models import record

import peewee

db = peewee.MySQLDatabase(None)


def init_db():
    db.init(DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
    db.connect()
    db.create_tables([record.Record])


def close_db():
    db.close()
