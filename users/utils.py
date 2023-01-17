import base64

from django.http import (
    HttpRequest, HttpResponse
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import ProfileForm
from .exceptions import UsersValidationException


def verify_login_request(request: HttpRequest):
    """
    Raises:
        UsersValidationException: Contains HttpResponse with error message.
    """
    if request.user.is_authenticated:
        raise UsersValidationException(
            HttpResponse('Already logged in')
        )

    if not has_basic_auth(request):
        raise UsersValidationException(
            HttpResponse('No auth header', status=401)
        )


def verify_register_request(request: HttpRequest):
    """
    Raises:
        UsersValidationException: Contains HttpResponse with error message.
    """
    verify_login_request(request)  # omg

    uname, _ = get_basic_auth_creds(request)
    if User.objects.filter(username=uname):
        raise UsersValidationException(
            HttpResponse('User already exists')
        )


def has_basic_auth(request: HttpRequest):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            return True

    return False


def get_basic_auth_creds(request: HttpRequest):
    auth = request.META['HTTP_AUTHORIZATION'].split()
    uname, passwd = base64.b64decode(auth[1].encode()).decode().split(':')
    return (uname, passwd)


def create_user(uname: str, passwd: str) -> User:
    userForm = create_user_form(uname, passwd)
    if not userForm.is_valid():
        raise UsersValidationException(
            HttpResponse('Invalid user form')
        )
    return userForm.save()


def create_user_form(uname, passwd) -> UserCreationForm:
    userForm = UserCreationForm({
        'username': uname,
        'password1': passwd,
        'password2': passwd,
    })

    return userForm


def create_profile_from_user(user: User):
    form = ProfileForm(user).save(commit=False)
    form.user = user
    form.save()
