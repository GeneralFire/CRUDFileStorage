from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Profile
        fields = ['user', 'file_uploaded']
