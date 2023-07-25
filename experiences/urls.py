from django.urls import path
from . import views

urlpatterns = [
    path("", views.Experiences.as_view()),
]
