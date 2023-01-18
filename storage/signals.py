from .minio_adapter import minio_adapter

from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from .models import File


@receiver(pre_delete, sender=File)
def file_delete_signal(sender, instance: File, **kwargs):
    minio_adapter.delete(str(instance.id))
