from .models import File

from django.http import (
    HttpRequest, HttpResponseBadRequest,

)
from django.contrib.auth.hashers import make_password, check_password


ACCESS_KEY = 'access_key'


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


def is_upload_file_request_valid(request: HttpRequest):
    """
    Raises:
        HttpResponseBadRequest: in case request without files,
            or request doesn't contains access key and sent by not
            authorized user.
    """
    if not request.FILES:
        return HttpResponseBadRequest()

    by_authorized_user = True if request.user.is_authenticated else False
    access_key = get_access_key_from_cookies(request)

    # set at least one access capability
    if not (by_authorized_user or access_key):
        return HttpResponseBadRequest()
