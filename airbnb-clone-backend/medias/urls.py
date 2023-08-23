from django.urls import path
from .views import PhotoDetail

urlpatterns = [
    path("photo/<int:pk>", PhotoDetail.as_view()),
]
