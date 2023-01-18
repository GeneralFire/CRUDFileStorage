from rest_framework import serializers

from storage.models import File
from users.models import Profile


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.CharField()

    class Meta:
        model = File
        fields = ['title', 'description', 'size',
                  'owner', 'id', 'download_count']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Profile
        fields = ['user', 'files_uploaded']
