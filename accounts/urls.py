from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.custom_login_view, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("settings/", views.user_settings, name="user_settings"),
    path("watchlist/", views.view_watchlist, name="watchlist"),
]
