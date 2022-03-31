from django.urls import path
from . import views

# Register views for login,logout and register
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # User verification
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
]
