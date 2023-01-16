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

ENTRYPOINT ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
