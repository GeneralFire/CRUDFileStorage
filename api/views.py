import base64

from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.core.exceptions import BadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

from storage.serializers import FileSerializer
from storage.models import File
from storage.views import upload_file, delete_file, download_file
from storage.minio_adapter import minio_adapter

from users.serializers import ProfileSerializer
from users.models import Profile
from users.utils import create_user, get_basic_auth_creds, has_basic_auth

# https://webdevblog.ru/sozdanie-django-api-ispolzuya-django-rest-framework-apiview/


class StorageApiView(APIView):
    def get(self, request: HttpRequest, *args, **kwargs):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def delete(self, request: HttpRequest, *args, **kwargs):
        try:
            pk = get_pk_from_kwargs(kwargs)
            delete_file(request, pk)
            return Response()
        except BadRequest as e:
            return

    def link(self, request: HttpRequest, *args, **kwargs):
        pk = kwargs.get('pk', '')
        if not pk:
            return response_with_reason(
                f"Ivalid file id '{pk}'"
            )

        try:
            file = File.objects.get(id=pk)
        except File.DoesNotExist:
            return response_with_reason(
                f'File with id {pk} not found',
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_access_allowed(request, file):
            return response_with_reason(
                'You not allowed to download this file',
                status=status.HTTP_403_FORBIDDEN)

        return Response(minio_adapter.get_file(pk))

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            upload_file(request)
        except BadRequest as e:
            return response_with_reason(
                f'{e}',
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfilesApiView(APIView):
    def get(self, request: HttpRequest):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class AuthApiView(APIView):
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return response_with_reason(
                'Already authenticated',
                status=status.HTTP_208_ALREADY_REPORTED
            )

    def delete(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
            return Response()
        return response_with_reason(
            'Already logged out',
            status=status.HTTP_401_UNAUTHORIZED
        )


def get_pk_from_kwargs(kwargs: dict):
    return kwargs.get('pk', '')


@api_view(['POST'])
def register(request: HttpRequest):
    if not has_basic_auth(request):
        return Response(
            'Invalid basic auth field',
            status=status.HTTP_400_BAD_REQUEST
        )
    uname, passwd = get_basic_auth_creds(request)
    try:
        create_user(uname, passwd)
        return Response()
    except Exception as e:
        return response_with_reason(
            f'{e}',
            status=status.HTTP_400_BAD_REQUEST
        )


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
