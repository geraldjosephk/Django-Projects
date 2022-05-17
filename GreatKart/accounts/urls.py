from django.urls import path
from . import views

# Register views for login,logout and register
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.dashboard, name="dashboard"),
    # User verification
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("forgotPassword", views.forgotPassword, name="forgotPassword"),
    path(
        "resetpassword_validate/<uidb64>/<token>/",
        views.resetpassword_validate,
        name="resetpassword_validate",
    ),
    path("resetPassword", views.forgotPassword, name="resetPassword"),
    # Orders
    path("my_orders/", views.my_orders, name="my_orders"),
    # Edit profile
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]
