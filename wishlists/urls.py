from django.urls import path
from . import views

urlpatterns = [
    path("", views.WishLists.as_view()),
    path("<int:pk>/", views.WishListDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>/", views.WishlistToggle.as_view()),
]
