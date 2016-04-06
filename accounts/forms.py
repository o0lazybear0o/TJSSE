from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
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
        required=True,
        label="Password",
        error_messages={'required': '请输入密码'},
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

class ChangeStudentInfoForm(ModelForm):
    first_name = forms.CharField(
        required=True,
        label="FirstName",
        error_messages={'required': '请输入名字'},
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "FirstName",
                'style': "width: 100%",
            }
        ),
    )

    last_name = forms.CharField(
        required=True,
        label="LastName",
        error_messages={'required': '请输入姓氏'},
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': "LastName",
                'style': "width: 100%",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        label="E-mail",
        error_messages={'required': '请输入姓氏'},
    )

    class Meta:
        model = UserProfile
        fields = ['grade', 'major', 'phone']



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
