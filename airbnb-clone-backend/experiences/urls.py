from django.urls import path
from . import views

urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>/", views.ExperiencesDetail.as_view()),
    path("<int:pk>/perks/", views.ExperiencePerk.as_view()),
    path("<int:pk>/bookings/", views.ExperienceBooking.as_view()),
    path("<int:pk>/bookings/<int:booking_pk>", views.ExperienceDetailBooking.as_view()),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>/", views.PerkDetail.as_view()),
]
