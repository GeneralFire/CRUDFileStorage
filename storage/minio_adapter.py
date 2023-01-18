import os
import io

import minio
from django.core.files import File

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

    def save(self, id: str, file_stream: io.BytesIO) -> str:
        """Return error message if error.
        """
        try:
            self._minio.put_object(
                MinioAnonAdapter.DEFAULT_BACKET_NAME,
                id,
                file_stream,
                file_stream.size,
                content_type=file_stream.content_type
            )
            return ''
        except Exception as e:
            return str(e)

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
