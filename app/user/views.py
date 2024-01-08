from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import CustomUserCreationForm


class UserListView(ListView):
    model = User
    template_name = "user/user_list.html"
    # permission_required = "auth.view_user"


class UserCreateView(PermissionRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm  # Use Django's built-in UserCreationForm
    template_name = "user/user_form.html"
    success_url = reverse_lazy("user-list")
    permission_required = "auth.add_user"


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm  # Use Django's built-in UserChangeForm
    template_name = "user/user_form.html"
    success_url = reverse_lazy("user-list")
    permission_required = "auth.change_user"


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy("user-list")
    permission_required = "auth.delete_user"
