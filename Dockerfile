FROM python:3.8-bullseye

ENV PYTHONUNBUFFERED=1 \ 
    POETRY_VERSION=1.1.14

WORKDIR /app
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /app/
RUN poetry export -f requirements.txt --without-hashes > requirements.txt
RUN pip install -r requirements.txt
RUN apt update 
RUN apt install -y \
    iputils-ping \
    net-tools \
    iproute2

COPY migrate_and_runserver.sh /app/
ENTRYPOINT ["bash", "/app/migrate_and_runserver.sh"]
