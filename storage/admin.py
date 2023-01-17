from django.contrib import admin

# Register your models here.

from .models import File, Review, Tag

admin.site.register(
    [File, Review, Tag]
)
