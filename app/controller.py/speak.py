from app.models import speak


"""
    1. Get the text size, if greater, return error
    2. submit the task to dramatiq
    3. insert into database (id, task_id, service, callback, speed, status, download_url, created_at, updated_at)
"""


def speak(request: speak.SpeakRequest):
    pass
