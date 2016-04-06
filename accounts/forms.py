from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="UserName",
        error_messages={'required': '请输入用户名'},
    )
    password = forms.CharField(
        required=True,
        label="Password",
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()


class ChangeStudentInfoForm(ModelForm):
    first_name = forms.CharField(
        required=True,
        label="FirstName",
        error_messages={'required': '请输入名字'},
    )

    last_name = forms.CharField(
        required=True,
        label="LastName",
        error_messages={'required': '请输入姓氏'},
    )

    email = forms.EmailField(
        required=True,
        label="E-mail",
        error_messages={'required': '请输入邮箱地址'},
    )

    class Meta:
        model = UserProfile
        fields = ['grade', 'major', 'phone']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        label="Old Password",
        error_messages={'required': '请输入旧密码'},
        widget=forms.PasswordInput(),
    )
    new_password = forms.CharField(
        required=True,
        label="New Password",
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(),
    )
    new_password_again = forms.CharField(
        required=False,
        label="New Password Again",
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
