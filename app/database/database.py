from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from app.models import record

import peewee


class Database:
    inited = False
    db = peewee.MySQLDatabase(None)

    def init_db(
        self,
        db_name=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
    ):
        self.db.init(db_name, host=host, port=port, user=user, password=password)
        self.db.connect()
        self.db.create_tables([record.Record])
        self.inited = True

    def close_db(self):
        self.db.close()


db = Database()
