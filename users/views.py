
from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse,
    HttpResponseForbidden, JsonResponse
)

from django.contrib.auth import login, authenticate, logout

from .models import Profile
from .serializers import ProfileSerializer
from .utils import (
    verify_login_request, verify_register_request,
    verify_logout_request, get_basic_auth_creds,
    create_profile_from_user, create_user
)
from crudfilestorage.badrequest_handler import badrequest_to_http_response


@badrequest_to_http_response
@require_http_methods(["GET"])
def get_profiles(request: HttpRequest):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return JsonResponse(serializer.data, safe=False)


@badrequest_to_http_response
@require_http_methods(["POST"])
def login_user(request: HttpRequest):
    verify_login_request(request)

    uname, passwd = get_basic_auth_creds(request)
    user = authenticate(request, username=uname, password=passwd)

    if user:
        login(request, user)
        return HttpResponse('Login success')

    return HttpResponseForbidden('Invalid username/password')


@badrequest_to_http_response
@require_http_methods(["POST"])
def logout_user(request: HttpRequest):
    verify_logout_request(request)
    logout(request)
    return HttpResponse('Logged out')


@badrequest_to_http_response
@require_http_methods(["POST"])
def register(request: HttpRequest):
    verify_register_request(request)

    uname, passwd = get_basic_auth_creds(request)
    user = create_user(uname, passwd)
    create_profile_from_user(user)
    login(request, user)
    return HttpResponse('Registered successfuly')
