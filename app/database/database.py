from contextvars import ContextVar

import peewee

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.MySQLDatabase(
    DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD
)
db._state = PeeweeConnectionState()
