from django.urls import path

from . import views
urlpatterns = [
    path('upload', views.upload_file),
    path('download/<str:pk>/', views.download_file)

]
