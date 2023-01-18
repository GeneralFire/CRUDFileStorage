from django.urls import path

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
    path('user', views.UserViewSet.as_view(
        {
            'post': 'login',
            'delete': 'logout',
            'put': 'register',
        }
    )),
    path('', views.get_api_routines)
]
