import uuid

from django.db import models
from django.core.files.uploadedfile import UploadedFile

from users.models import Profile
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
        Profile, on_delete=models.CASCADE, blank=True, null=True)
    access_key = models.TextField(
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.title}/{self.id}'

    def get_stream(self):
        self.increment_download_count()
        return minio_adapter.get_file(str(self.id))

    def increment_download_count(self):
        self.download_count += 1
        self.save()

    def save(self, file: UploadedFile = None, *args, **kwargs):
        if file is not None:
            minio_adapter.save(str(self.id), file=file)
            self.title = file.name
            self.size = file.size
        if self.owner:
            self.owner.increment_uploaded_files_count()
        super(File, self).save(*args, **kwargs)
