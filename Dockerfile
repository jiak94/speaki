# syntax=docker/dockerfile:1.3-labs
FROM python:3.10.5

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    adduser --disabled-password --gecos "" speaki && \
    adduser speaki sudo

RUN mkdir /tts

RUN chown speaki /tts

USER speaki
WORKDIR /home/speaki

ENV PYTHONUNBUFFERED 1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/home/speaki/.local/bin


COPY --chown=speaki pyproject.toml poetry.lock ./

RUN poetry install

COPY --chown=speaki ./ ./

ENTRYPOINT [ "./entrypoint.sh" ]
