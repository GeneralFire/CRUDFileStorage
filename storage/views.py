from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse, HttpResponseNotAllowed,
    HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError, HttpResponseBadRequest,
    StreamingHttpResponse
)

from .utils import (
    is_access_allowed, get_access_key_from_cookies,
    is_upload_file_request_valid
)
from .models import File
from .forms import FileForm
from . import minio


@require_http_methods(["POST"])
def upload_file(request: HttpRequest):
    is_upload_file_request_valid(request)

    file = File()
    fileForm = FileForm(request.POST)

    try:
        size = minio.save(file.id, request.FILES['file'])
        file: File = fileForm.save(commit=False)
        file.size = size
        if request.user.is_authenticated:
            file.owner = request.user
        access_key = get_access_key_from_cookies(request)
        if access_key:
            file.access_key = access_key

        fileForm.is_valid() and fileForm.save()
    except:
        return HttpResponseServerError()

    return HttpResponse(f'{file.id}')


@require_http_methods(["GET"])
def download_file(request: HttpRequest, pk: str):
    try:
        file = File.objects.get(id=pk)
    except:
        return HttpResponseNotFound()

    if not is_access_allowed(request, file):
        return HttpResponseForbidden()

    stream = minio.get_file_stream(pk)
    return StreamingHttpResponse(stream)


@require_http_methods(["DELETE"])
def delete_file(request: HttpRequest, pk: str):
    try:
        file = File.objects.get(id=pk)
    except:
        return HttpResponseNotFound()

    if not is_access_allowed(request, file):
        return HttpResponseForbidden()

    minio.delete(pk)
    file.delete()
    return HttpResponse()
