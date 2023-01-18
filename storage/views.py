from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse, StreamingHttpResponse
)

from .utils import (
    verify_upload_request, verify_download_request,
    verify_delete_request, get_formdata_enc_access_key_from_get_request
)
from .models import File
from .forms import FileForm
from crudfilestorage.badrequest_handler import badrequest_to_http_response
from .minio_adapter import minio_adapter


@badrequest_to_http_response
@require_http_methods(["POST"])
def upload_file(request: HttpRequest):
    verify_upload_request(request)

    fileForm = FileForm(request.POST)
    if not fileForm.is_valid():
        return HttpResponse('Invalid file form-data', status=400)

    file: File = fileForm.save(commit=False)

    file_to_upload = request.FILES['file']
    if not file_to_upload.size:
        return HttpResponse(
            'Empty file upload attempt', status=400
        )
    err_msg = minio_adapter.save(str(file.id), request.FILES['file'])
    if err_msg:
        return HttpResponse(
            f'Error occur while uploading: {err_msg}', status=400
        )

    file.title = file_to_upload.name
    file.size = file_to_upload.size
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
    file = minio_adapter.get_file(pk)
    return StreamingHttpResponse(file)


@badrequest_to_http_response
@require_http_methods(["DELETE"])
def delete_file(request: HttpRequest, pk: str):
    verify_delete_request(request, pk)

    file = File.objects.get(id=pk)
    file.delete()
    minio_adapter.delete(pk)

    return HttpResponse('File deleted')
