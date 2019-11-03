from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext
import re
from .models import Category, Institution, Donation, TYP


def validate_password(value):
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if len(value) < 8:
        raise ValidationError(ugettext('Hasło musi być dłuższe niż 8 znaków!'))
    if not any(char.isdigit() for char in value):
        raise ValidationError(ugettext('Hasło musi zawierać przynajmniej 1 liczbę!'))
    if not any(char.islower() for char in value):
        raise ValidationError(ugettext('Hasło musi zawierać przynajmniej 1 małą literę!'))
    if not any(char.isupper() for char in value):
        raise ValidationError(ugettext('Hasło musi zawierać przynajmniej 1 dużą literę!'))
    if not any(char in special_characters for char in value):
        raise ValidationError(ugettext('Hasło musi zawierać przynajmnniej 1 znak specjalny'))

# class AddUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'password' 'num_vote_up', 'num_vote_down', 'vote_score']

class RegisterUserForm(forms.Form):
    first_name = forms.CharField(label="Imię", max_length=30)
    last_name = forms.CharField(label="Nazwisko", max_length=40)
    email = forms.EmailField(label="Email", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło", max_length=12, validators=[validate_password])
    password_again = forms.CharField(widget=forms.PasswordInput(), label="Powtórz hasło", max_length=12, validators=[validate_password])
    #log_on = forms.BooleanField(label="Logowanie po rejestracji:",required=False)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło", max_length=12)

class AddDonationForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Category.objects.all())
    quantity = forms.IntegerField(min_value=0, max_value=100)
    institution = forms.ModelChoiceField(queryset=Institution.objects.all())
    adress = forms.CharField(max_length=250)
    city = forms.CharField(max_length=60)
    zip_code = forms.CharField(max_length=6)
    phone_number = forms.CharField(max_length=11)
    pick_up_date = forms.DateField(widget=forms.SelectDateWidget)
    pick_up_time = forms.TimeField(widget=forms.TimeInput)
    pick_up_comment = forms.CharField(widget=forms.Textarea, max_length=400)
    
class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="Hasło", max_length=10)

class UserEditForm(forms.Form):
    first_name = forms.CharField(label="Nowe imię", max_length=30, required=False)
    last_name = forms.CharField(label="Nowe nazwisko", max_length=40, required=False)

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label="wprowadź nowe hasło")
    new2_password = forms.CharField(widget=forms.PasswordInput(), label="powtórz nowe hasło")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=64, label="Imię i nazwisko")
    surname = forms.EmailField(label="Email", max_length=64)
    message = forms.CharField(widget=forms.Textarea, max_length=500, label="Wpisz treść wiadomości")



