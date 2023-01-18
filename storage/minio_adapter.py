import os
import io

import minio

from django.core.files.uploadedfile import InMemoryUploadedFile


__all__ = ['minio_adapter']


class MinioAnonAdapter:

    DEFAULT_BACKET_NAME = 'main'

    def __init__(self):
        url = os.getenv('MINIO_URL')

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

    def save(self, id: str, fileStream: io.BytesIO) -> str:
        """Return error message if error.
        """
        try:
            self._minio.put_object(
                MinioAnonAdapter.DEFAULT_BACKET_NAME,
                id,
                fileStream,
                fileStream.size,
                content_type=fileStream.content_type
            )
            return ''
        except Exception as e:
            return str(e)

    def get_file_response(self, id: str):
        return self._minio.get_object(
            MinioAnonAdapter.DEFAULT_BACKET_NAME,
            id
        )


minio_adapter = MinioAnonAdapter()
