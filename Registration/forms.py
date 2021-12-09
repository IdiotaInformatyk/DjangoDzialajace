from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Wykorzystanie podstawki od Django do tworzenia urzytkowników
# EmailField wykorzystuje EmailValidator zeby sprawdzić poprawność zapisu emailu


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]