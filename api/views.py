from django.contrib.auth import login, logout
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from storage.serializers import FileSerializer
from storage.models import File
from storage.utils import is_access_allowed

from users.serializers import ProfileSerializer
from users.models import Profile

# https://webdevblog.ru/sozdanie-django-api-ispolzuya-django-rest-framework-apiview/


class StorageApiView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def delete(self, request: HttpRequest, *args, **kwargs):
        pk = get_pk_from_kwargs(kwargs)
        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return response_with_reason(
                f'File with id {pk} not found',
                status=status.HTTP_404_NOT_FOUND
            )

        file.delete()
        return Response()

    def link(self, request: HttpRequest, *args, **kwargs):
        pk = self.kwargs.get('pk', '')
        if pk:
            pass

    def post(self, request: HttpRequest, *args, **kwargs):
        pass


class ProfilesApiView(APIView):
    def get(self, request: HttpRequest):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class AuthApiView(APIView):
    def post(self, request: HttpRequest):
        auth = self.get_authenticate_header()
        pass

    def delete(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
            return Response('Ok')
        return Response('Already logged out')


def get_pk_from_kwargs(kwargs: dict):
    return kwargs.get('pk', '')


def get_access_key_from_kwargs(kwargs: dict):
    return kwargs.get('pk', '')


@api_view(['POST'])
def register(request: HttpRequest):
    pass

@api_view(['GET'])
def get_api_routines(request: HttpRequest):
    routines = {
        '/storage': {
            'GET': 'List files',
            'POST': 'Upload file',
        },
        '/storage/*': {
            'DELETE': 'Delete file by id',
            'LINK': 'Download file by id',
        },
        '/profiles': {
            'GET': 'List profiles'
        },
        '/auth': {
            'POST': 'Login using basic auth',
            'DELETE': 'Logout'
        },
        '/register': {
            'Register using base auth'
        },
        '/': {
            'GET': 'List available API routines'
        }

    }
    return Response(routines)


def response_with_reason(reason: str, status: status):
    return Response(
        {'Reson': reason},
        status=status
    )
