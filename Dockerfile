FROM python:3.10.5

RUN mkdir /tts

WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install poetry

COPY . /code

RUN poetry install

RUN poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
