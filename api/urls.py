from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

storage_router = DefaultRouter(trailing_slash=False)
storage_router.register(r'storage', views.StorageViewSet, 'storage', )
urlpatterns = [
    path('profiles', views.ProfilesViewSet.as_view(
        {
            'get': 'list'
        }
    )),
    path('register', views.register),
    path('token', obtain_auth_token),
    path('', views.get_api_routines)
] + storage_router.urls
