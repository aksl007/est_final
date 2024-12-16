from django.urls import path
from . import views

app_name = 'emotion_tracker'
urlpatterns = [
    path('', views.index, name='index'),
    path("upload/", views.upload, name="upload"),
    path("detail/", views.detail, name="detail"),
    path('upload/download_video/', views.download_video, name='download_video'),
    path('upload/frames/<str:filename>/', views.serve_frame, name='serve_frame'),
]