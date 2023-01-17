import os

import minio

from django.core.files.uploadedfile import InMemoryUploadedFile


MINIO_URL = os.getenv('MINIO_URL', 'localhost:9000')
ACCESS_KEY = os.getenv('MINIO_AK')
SECRET_KEY = os.getenv('MINIO_SK')

MINIO_CLIENT = minio.Minio(
    MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)


def delete(identifier: str):
    pass


def save(id: str, stream: InMemoryUploadedFile) -> int:
    """_summary_

    Args:
        id (str): S3 File identier.
        stream (InMemoryUploadedFile): Download stream

    Returns:
        int: _description_
    """
    handle_uploaded_file(stream)
    return 3  # TODO: fix me


def handle_uploaded_file(f):
    total_chunks = 0
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            total_chunks += destination.write(chunk)
    return total_chunks


def get_file_stream(id):
    f = open('name.txt', 'rb')
    return f
