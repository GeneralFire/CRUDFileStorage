
from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse,
    HttpResponseForbidden, JsonResponse
)

from django.contrib.auth import login, authenticate, logout

from .models import Profile
from .serializers import ProfileSerializer
from .utils import (
    verify_login_request, get_basic_auth_creds,
    create_profile_from_user, verify_register_request,
    create_user
)
from .exceptions import UsersValidationException


@require_http_methods(["GET"])
def get_profiles(request: HttpRequest):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return JsonResponse(serializer.data, safe=False)


@require_http_methods(["POST"])
def login_user(request: HttpRequest):
    try:
        verify_login_request()
    except UsersValidationException as e:
        return e

    uname, passwd = get_basic_auth_creds(request)
    user = authenticate(request, username=uname, password=passwd)

    if user:
        login(request, user)
        return HttpResponse('Login success')

    return HttpResponseForbidden('Invalid username/password')


@require_http_methods(["POST"])
def logout_user(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponse('User not logged in')
    logout(request)
    return HttpResponse('Logged out')


@require_http_methods(["POST"])
def register(request: HttpRequest):
    try:
        verify_register_request(request)
    except UsersValidationException as e:
        return e

    uname, passwd = get_basic_auth_creds(request)
    user = create_user(uname, passwd)
    create_profile_from_user(user)
    login(request, user)
    return HttpResponse()
