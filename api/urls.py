from django.urls import path

from . import views

urlpatterns = [
    path('storage', views.StorageApiView.as_view()),
    path('storage/<str:pk>', views.StorageApiView.as_view()),
    path('profiles', views.ProfilesApiView.as_view()),
    path('auth', views.AuthApiView.as_view()),
    path('register', views.register),
    path('', views.get_api_routines)
]
