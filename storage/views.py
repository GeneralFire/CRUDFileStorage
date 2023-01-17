
from django.http import (
    HttpRequest, HttpResponse, HttpResponseNotAllowed,
    HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError, HttpResponseBadRequest,
    StreamingHttpResponse
)

from .models import File
from .forms import FileForm
from . import minio


def upload_file(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

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


def download_file(request: HttpRequest, pk: str):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    try:
        file = File.objects.get(id=pk)
    except:
        return HttpResponseNotFound()

    if file.owner:
        if request.user != file.owner:
            return HttpResponseForbidden()

    stream = minio.get_file_stream(pk)
    return StreamingHttpResponse(stream)
