from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    CustomLoginView,
    CustomPasswordChangeView,
    ChangePasswordView,
)

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path(
        "accounts/password/change/",
        CustomPasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path(
        "ChangePasswordView/<int:pk>/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
]
