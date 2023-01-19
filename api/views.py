from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, FileResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .serializers import FileSerializer
from storage.forms import FileForm
from storage.models import File

from .serializers import ProfileSerializer, FileSerializer
from users.models import Profile


class StorageViewSet(viewsets.ViewSet):

    FILE_ACCESS_KEY = 'access_key'
    FILE_KEY = 'file'

    def list(self, request: HttpRequest):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def destroy(self, request: HttpRequest, pk: str):
        queryset = File.objects.all()
        file = get_object_or_404(queryset, pk=pk)
        if not self._is_allowed_to_access(request, file):
            return self._return_forbidden(pk)
        file.delete()
        return Response()

    def retrieve(self, request: HttpRequest, pk):
        queryset = File.objects.all()
        file = get_object_or_404(queryset, pk=pk)
        if not self._is_allowed_to_access(request, file):
            return self._return_forbidden(pk)
        return FileResponse(
            file.get_stream(),
            filename=file.title,
        )

    def create(self, request: HttpRequest, *args, **kwargs):
        if not self._met_access_capability(request):
            return response_with_reason(
                'Use access_key form-data or authorize to upload file',
                status.HTTP_401_UNAUTHORIZED
            )
        if not self._is_upload_request_valid(request):
            return response_with_reason(
                'File request invalid. Check file form-data',
                status.HTTP_400_BAD_REQUEST
            )

        fileForm = FileForm(request.POST)
        file: File = fileForm.save(commit=False)
        self._set_access_fields(request, file)

        try:
            file.save(
                file=request.FILES[StorageViewSet.FILE_KEY]
            )
        except ValidationError as e:
            return response_with_reason(
                f'Unable to validate file: {e}',
                status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'File id': str(file.id)}
        )

    def _met_access_capability(self, request: HttpRequest):
        if request.user.is_authenticated:
            return True
        return request.POST.get(StorageViewSet.FILE_ACCESS_KEY, '')

    def _is_upload_request_valid(self, request: HttpRequest):
        if not request.FILES:
            return False
        if StorageViewSet.FILE_KEY not in request.FILES:
            return False
        if not request.FILES[StorageViewSet.FILE_KEY].size:
            return False
        return True

    def _set_access_fields(self, request: HttpRequest, file: File):
        if request.user.is_authenticated:
            file.owner = request.user
        file.access_key = make_password(
            request.FILES.get(StorageViewSet.FILE_ACCESS_KEY, '')
        )

    def _is_allowed_to_access(self, request: HttpRequest, file: File):
        if file.owner:
            if not request.user.is_authenticated:
                return False
            if request.user == file.owner:
                return True

        if not file.access_key:
            return False

        request_access_key = request.META.get(
            StorageViewSet.FILE_ACCESS_KEY, ''
        )
        if check_password(
            request_access_key,
            file.access_key
        ):
            return True

        return False

    def _return_forbidden(self, pk):
        return response_with_reason(
            f"You unable to access this '{pk}' file",
            status=status.HTTP_403_FORBIDDEN
        )


class ProfilesViewSet(viewsets.ViewSet):
    def list(self, request: HttpRequest):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def register(request: HttpRequest):
    """Form-data request based registraton."""
    userForm = UserCreationForm(request.POST)
    if not userForm.is_valid():
        return Response(
            userForm.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    userForm.save()
    return Response()


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
        '/token': {
            'POST': 'Get token',
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
        {
            'Reason': reason
        },
        status=status
    )
