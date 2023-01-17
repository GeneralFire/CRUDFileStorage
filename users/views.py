import base64

from django.views.decorators.http import require_http_methods
from django.http import (
    HttpRequest, HttpResponse, HttpResponseNotAllowed,
    HttpResponseForbidden, HttpResponseNotFound,
    JsonResponse
)

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from .forms import ProfileForm
from .serializers import ProfileSerializer
# Create your views here.


def get_profiles(request: HttpRequest):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return JsonResponse(serializer.data, safe=False)


@require_http_methods(["POST"])
def login_user(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponse('Already logged in')

    if 'HTTP_AUTHORIZATION' not in request.META:
        return HttpResponse('No auth header', status=401)

    uname, passwd = _extract_uname_passwd_from_auth(
        request.META['HTTP_AUTHORIZATION']
    )

    try:
        user = User.objects.get(username=uname)
    except:
        return HttpResponseNotFound('User not found')

    user = authenticate(request, username=uname, password=passwd)

    if user:
        login(request, user)
        return HttpResponse('Login success')

    return HttpResponseForbidden('Invalid pass')


@require_http_methods(["POST"])
def logout_user(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponse('User not logged in')
    logout(request)
    return HttpResponse('Logged out')


@require_http_methods(["POST"])
def register(request: HttpRequest):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return HttpResponse('No auth header', status=401)

    uname, passwd = _extract_uname_passwd_from_auth(
        request.META['HTTP_AUTHORIZATION'])

    if User.objects.filter(username=uname):
        return HttpResponse('User already exists')

    userForm = _create_user_form(uname, passwd)
    if not userForm.is_valid():
        return HttpResponse('Invalid user form')

    userForm.save()
    # login(request, uname)
    user = authenticate(request, username=uname, password=passwd)
    _save_profile(user)
    return HttpResponse()


def _extract_uname_passwd_from_auth(auth):
    auth = auth.split()
    uname, passwd = base64.b64decode(auth[1].encode()).decode().split(':')
    return (uname, passwd)


def _create_user_form(uname, passwd) -> UserCreationForm:
    userForm = UserCreationForm(
        {
            'username': uname,
            'password1': passwd,
            'password2': passwd,
        }
    )

    return userForm


def _save_profile(user):
    form = ProfileForm(user).save(commit=False)
    form.user = user
    form.save()
