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


class ChangeUserInfoForm(ModelForm):
    first_name = forms.CharField(
        required="True",
        error_messages={'required': '姓氏'},
    )
    last_name = forms.CharField(
        required="True",
        error_messages={'required': '名字'},
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ChangeStudentInfoForm(ModelForm):
    grade = forms.IntegerField(
        required="True",
        error_messages={'required': '年级'},
    )
    class Meta:
        model = UserProfile
        exclude = ['user', 'type']


class ChangeProfessorInfoForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']


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
