from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=50)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation de mot de passe', widget=forms.PasswordInput)

    # user clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = User.objects.filter(username__exact=username)
        if len(filter_result) > 0:
            raise forms.ValidationError('Cet identifiant existe déjà')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Cet email existe déjà")
        else:
            raise forms.ValidationError("Veuillez saisir un email valide")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Non-correspondance du mot de passe, veuillez saisir à nouveau')

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=50)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    # use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("Cet email n'existe pas")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("Ce nom d'utilisateur n'existe pas, veuillez d'abord vous inscrire")

        return username


class ProfileForm(forms.Form):
    email = forms.EmailField(label='Email')

