from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver

from .models import Profile


@receiver(post_save, sender=User)
def profile_creation_signal(sender, instance: User, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=instance)
