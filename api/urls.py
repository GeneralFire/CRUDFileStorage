from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('storage', views.StorageViewSet.as_view(
        {
            'get': 'list',
            'delete': 'delete',
            'post': 'upload',
            'link': 'download'
        },
    )),
    path('profiles', views.ProfilesViewSet.as_view(
        {
            'get': 'list'
        }
    )),
    path('register', views.register),
    path('token', obtain_auth_token),
    path('', views.get_api_routines)
]
