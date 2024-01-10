from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class CustomUserCreationForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select groups for the user.",
    )

    class Meta:
        model = User
        fields = ("username", "password", "groups")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()

            # Add user to selected groups
            groups = self.cleaned_data.get("groups")
            if groups:
                user.groups.set(groups)

        return user
    
class ChangePasswordForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("password",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user
