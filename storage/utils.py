from .models import File

from django.http import HttpRequest
from django.core.exceptions import BadRequest
from django.contrib.auth.hashers import check_password, make_password


ACCESS_KEY = 'access_key'


def get_formdata_enc_access_key_from_get_request(request: HttpRequest):
    request_data = request.POST
    if ACCESS_KEY in request_data:
        return make_password(request_data[ACCESS_KEY])
    return ''


def get_access_key_from_cookies(request: HttpRequest):
    request_meta = request.COOKIES
    if ACCESS_KEY in request_meta:
        return request_meta[ACCESS_KEY]
    return ''


def is_access_allowed(request: HttpRequest, file: File):
    if file.owner:
        if not request.user.is_authenticated:
            return False
        if request.user == file.owner:
            return True

    if not file.access_key:
        return False

    request_access_key = get_access_key_from_cookies(request)
    if check_password(
        request_access_key,
        file.access_key
    ):
        return True

    return False


def verify_upload_request(request: HttpRequest):
    """
    Raises:
        BadRequest: in case request without files,
            or request doesn't contains access key and sent by not
            authorized user.
    """
    if not request.FILES or 'file' not in request.FILES:
        raise BadRequest("Request doesn't contains files/no file form-data")

    by_authorized_user = True if request.user.is_authenticated else False
    access_key = get_formdata_enc_access_key_from_get_request(request)

    # set at least one access capability
    if not (by_authorized_user or access_key):
        raise BadRequest(
            'Authenticate or use access_key form-data to access file')


def verify_download_request(request: HttpRequest, pk: str):
    """
    Raises:
        BadRequest: In case file not exists or
            user unable to access it.
    """
    try:
        file = File.objects.get(id=pk)
    except:
        raise BadRequest('Requested file not found')

    if not is_access_allowed(request, file):
        raise BadRequest('You unable to access this file')


def verify_delete_request(request: HttpRequest, pk: str):
    verify_download_request(request, pk)    # TODO: not intuitive
