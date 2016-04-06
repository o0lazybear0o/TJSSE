from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        required=False,
        label="UserName",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "UserName",
                'style': "width: 100%",
            }
        ),
    )
    password = forms.CharField(
        required=False,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Password",
                'style': "width: 100%",
            }
        ),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

# class Student(forms.Form):
#     username = forms.CharField(disabled="true")


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=False,
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Old Password",
                'style': "width: 100%",
            }
        ),
    )
    new_password = forms.CharField(
        required=False,
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "New Password",
                'style': "width: 100%",
            }
        ),
    )
    new_password_again = forms.CharField(
        required=False,
        label="New Password Again",
        error_messages="",
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "New Password Again",
                'style': "width: 100%",
            }
        ),
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
