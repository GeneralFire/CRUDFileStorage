import uuid

from django.db import models


from users.models import User
# Create your models here.


class File(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    size = models.IntegerField(default=0, blank=False, null=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    access_count = models.IntegerField(default=0, editable=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    ratio = models.FloatField(default=0, blank=False, null=False)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    private = models.BooleanField(default=True, editable=True)

    def __str__(self):
        return f'{self.title}/{self.id}'

    def ready(self):
        from . import signals


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=256, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)

    def __str__(self):
        return self.name
