import io
import uuid

from django.db import models

from users.models import User
from .minio_adapter import minio_adapter
# Create your models here.


class File(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    size = models.IntegerField(default=0, blank=False, null=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0, editable=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    access_key = models.TextField(
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.title}/{self.id}'

    def get_stream(self):
        return minio_adapter.get_file(str(self.id))

    def increment_download_count(self):
        self.download_count += 1
        self.save()

    def save(self, title: str, file_stream: io.BytesIO, *args, **kwargs):
        minio_adapter.save(str(self.id), file_stream=file_stream)
        self.title = title
        super(File, self).save(*args, **kwargs)
