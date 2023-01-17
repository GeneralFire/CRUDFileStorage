from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse, HttpResponseForbidden,
    HttpResponseNotFound, HttpResponseServerError,
    StreamingHttpResponse
)

from .utils import (
    verify_upload_request, verify_download_request,
    verify_delete_request, get_formdata_enc_access_key_from_get_request
)
from .models import File
from .forms import FileForm
from crudfilestorage.badrequest_handler import badrequest_to_http_response
from . import minio


@badrequest_to_http_response
@require_http_methods(["POST"])
def upload_file(request: HttpRequest):
    verify_upload_request(request)

    # TODO: generate id without Model?
    fileForm = FileForm(request.POST)
    if not fileForm.is_valid():
        return HttpResponse('Invalid file form-data', status=400)

    file = File()
    size = minio.save(file.id, request.FILES['file'])
    if not size:
        return HttpResponse('Invalid file size', status=400)

    file.size = size
    if request.user.is_authenticated:
        file.owner = request.user
        request.user.profile.increment_uploaded_files_count()
    file.access_key = get_formdata_enc_access_key_from_get_request(request)
    file.save()
    return HttpResponse(f'File upload done. File id is {file.id}')


@badrequest_to_http_response
@require_http_methods(["GET"])
def download_file(request: HttpRequest, pk: str):
    verify_download_request(request, pk)
    stream = minio.get_file_stream(pk)
    return StreamingHttpResponse(stream)


@badrequest_to_http_response
@require_http_methods(["DELETE"])
def delete_file(request: HttpRequest, pk: str):
    verify_delete_request(request, pk)

    file = File.objects.get(id=pk)
    file.delete()
    minio.delete(pk)

    return HttpResponse('File deleted')
