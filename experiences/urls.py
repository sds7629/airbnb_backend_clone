from django.urls import path
from . import views

urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperiencesDetail.as_view()),
    path("perk/", views.Perks.as_view()),
    path("perk/<int:pk>", views.PerkDetail.as_view()),
]
