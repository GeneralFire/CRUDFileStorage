from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse, HttpResponseNotAllowed,
    HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError, HttpResponseBadRequest,
    StreamingHttpResponse
)

from .models import File
from .forms import FileForm
from . import minio


@require_http_methods(["POST"])
def upload_file(request: HttpRequest):
    if not request.FILES:
        return HttpResponseBadRequest()

    private = False if request.user.is_authenticated else True

    file = File()
    fileForm = FileForm(request.POST, private)

    try:
        size = minio.save(file.id, request.FILES['file'])
        file = fileForm.save(commit=False)
        file.size = size
        file.owner = request.user
        fileForm.is_valid() and fileForm.save()
    except:
        return HttpResponseServerError()

    return HttpResponse()


@require_http_methods(["GET"])
def download_file(request: HttpRequest, pk: str):
    try:
        file = File.objects.get(id=pk)
    except:
        return HttpResponseNotFound()

    if not _is_access_allowed(request.user, file):
        return HttpResponseForbidden()

    stream = minio.get_file_stream(pk)
    return StreamingHttpResponse(stream)


@require_http_methods(["DELETE"])
def delete_file(request: HttpRequest, pk: str):
    try:
        file = File.objects.get(id=pk)
    except:
        return HttpResponseNotFound()

    if not _is_access_allowed(request.user, file):
        return HttpResponseForbidden()

    minio.delete(pk)
    file.delete()
    return HttpResponse()


def _is_access_allowed(user, file):
    if file.owner:
        if user == file.owner:
            return True
    return False
