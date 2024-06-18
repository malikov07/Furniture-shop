from typing import Any
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

    def save(self, commit: bool = True):
        user = super().save(commit)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
