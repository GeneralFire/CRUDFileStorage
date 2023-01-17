from rest_framework import serializers

from .models import File, Tag, Review


class FileSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['title', 'description', 'size',
                  'owner', 'vote_total', 'ratio']

    def get_title(self, obj):
        return str(obj)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
