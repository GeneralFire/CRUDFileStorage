from . import minio

from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from .models import File


@receiver(pre_delete, sender=File)
def delete(sender, instance: File, **kwargs):
    minio.delete(instance.id)