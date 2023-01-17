from django.core.exceptions import BadRequest
from django.http import HttpResponse


def badrequest_to_http_response(func):
    def convert(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadRequest as e:
            return HttpResponse(e, status=400)

    return convert
