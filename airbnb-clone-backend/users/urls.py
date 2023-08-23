from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.LogOut.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogIn.as_view()),
    path("@<str:username>/", views.PublicUser.as_view()),
]
