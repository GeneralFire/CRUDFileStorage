from django.urls import path

from .import views

urlpatterns = [
    path('profiles', views.get_profiles),
    path('register', views.register),
    path('login', views.login_user),
    path('logout', views.logout_user),

]
