import os
import io

import minio
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile

__all__ = ['minio_adapter']


class MinioAnonAdapter:

    DEFAULT_BACKET_NAME = 'main'

    def __init__(self):
        url = os.getenv('MINIO_URL', 'localhost:9000')

        if not url:
            raise minio.S3Error('Cannot resolve MinIO url')

        self._minio = minio.Minio(
            url,
            secure=False
        )

    def delete(self, id):
        self._minio.remove_object(
            MinioAnonAdapter.DEFAULT_BACKET_NAME,
            id
        )

    def save(self, id: str, file: UploadedFile) -> str:
        self._minio.put_object(
            MinioAnonAdapter.DEFAULT_BACKET_NAME,
            id,
            file,
            file.size,
            content_type=file.content_type
        )

    def get_file(self, id: str) -> File:
        try:
            resp = self._minio.get_object(
                MinioAnonAdapter.DEFAULT_BACKET_NAME,
                id
            )
            file = File(file=io.BytesIO(resp.read()))
        finally:
            resp.close()
            resp.release_conn()
        return file


minio_adapter = MinioAnonAdapter()
