from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # password kiritganda hidden bolishi uchun

# User Registration Part

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Confirm", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):   # Shu yerda nafaqat password, barcha qismlarini validate qilish uchun clean methodini ishlatish mumkin edi.
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Parolingiz confirmationdan o'tmadi!")
        return data['password_2']

# EDIT qismi uchun 2 ta class ochib olamiz
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']