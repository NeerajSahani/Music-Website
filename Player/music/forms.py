from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LogForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user = self.cleaned_data.get('username')
        passw = self.cleaned_data.get('password')

        val = authenticate(username=user, password=passw)
        if not val:
            raise forms.ValidationError("Incorrect Credentials")


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'retype_password']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff']
