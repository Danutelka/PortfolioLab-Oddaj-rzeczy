from django import forms
from django.contrib.auth.models import User
from .models import Category, Institution, Donation, TYP

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Imię", max_length=32)
    last_name = forms.CharField(label="Nazwisko", max_length=64)
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło", max_length=10)
    password_again = forms.CharField(widget=forms.PasswordInput(), label="Powtórz hasło", max_length=10)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło", max_length=10)
