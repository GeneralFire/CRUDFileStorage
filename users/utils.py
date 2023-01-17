import base64

from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import ProfileForm
from .models import Profile
from django.core.exceptions import BadRequest


def verify_login_request(request: HttpRequest):
    """
    Raises:
        BadRequest: Contains HttpResponse with error message.
    """
    if is_authenticated(request):
        raise BadRequest('Already logged in')

    if not has_basic_auth(request):
        raise BadRequest('No auth header')


def is_authenticated(request: HttpRequest):
    return True if request.user.is_authenticated else False


def verify_logout_request(request: HttpRequest):
    if is_authenticated(request):
        raise BadRequest('Already logged in')

def verify_register_request(request: HttpRequest):
    """
    Raises:
        BadRequest: Contains HttpResponse with error message.
    """
    verify_login_request(request)  # omg

    uname, _ = get_basic_auth_creds(request)
    if User.objects.filter(username=uname):
        raise BadRequest('Username already registered')


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
        raise BadRequest('Invalid user form')
    return userForm.save()


def create_user_form(uname, passwd) -> UserCreationForm:
    userForm = UserCreationForm({
        'username': uname,
        'password1': passwd,
        'password2': passwd,
    })

    return userForm


def create_profile_from_user(user: User):
    form: Profile = ProfileForm(user).save(commit=False)
    form.user = user
    form.save()
