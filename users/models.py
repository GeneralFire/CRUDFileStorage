import uuid

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    file_uploaded = models.IntegerField(
        default=0, blank=False, null=False,
    )

    def __str__(self):
        return self.user.username

    def increment_uploaded_files_count(self):
        self.file_uploaded += 1
        self.save()
