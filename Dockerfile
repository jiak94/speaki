FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./docker/entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/web.sh /web
RUN chmod +x /web

COPY ./docker/worker.sh /worker
RUN chmod +x /worker

ENTRYPOINT [ "/entrypoint" ]
