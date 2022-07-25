from app.models.status import StatusResponse
from app.models import Code, Status
from app.models.record import Record
from peewee import DoesNotExist


def get_status(task_id: str) -> StatusResponse:
    response = StatusResponse(code=Code.OK)

    try:
        record: Record = Record.get(task_id=task_id)
        response.code = Code.OK
        response.msg = record.note
        match record.status:
            case Status.success:
                response.status = Status.success
                response.download_url = record.download_url
                return response
            case Status.failed:
                response.status = Status.failed
                return response
            case Status.processing:
                response.status = Status.processing
                return response
            case Status.pending:
                response.status = Status.pending
                return response
            case _:
                response.status = Status.unknown
                response.code = Code.BAD_REQUEST
                response.msg = "Unknown status"
                return response
    except DoesNotExist:
        response.code = Code.NOT_FOUND
        response.msg = "Record Not found"
        return response
    except:
        response.code = Code.INTERNAL_SERVER_ERROR
        response.msg = "Internal server error"
        return response
