from enum import IntEnum, Enum
import json
from pydantic import BaseModel


class Code(IntEnum):
    OK = 0
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    UNKNOWN = 999
    UNKNOWN_ERROR = 1000
    INVALID_TOKEN = 1001
    INVALID_USERNAME = 1002
    INVALID_PASSWORD = 1003
    INVALID_EMAIL = 1004
    INVALID_PHONE = 1005
    INVALID_NAME = 1006
    INVALID_BIRTHDAY = 100


class Service(str, Enum):
    azure = "azure"


class Speed(str, Enum):
    slow = "slow"
    normal = "normal"
    fast = "fast"


class Status(str, Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"
    unknown = "unknown"


class BaseModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.json()
        return json.JSONEncoder.default(self, o)
