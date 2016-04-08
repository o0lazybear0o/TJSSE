from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile
from django.contrib.auth.models import User
from project.models import Project, ProjectType


class NewStudent(forms.Form):
    start_id = forms.IntegerField(
        required=True,
        label="Start Id",
        error_messages={'required': '请输入起始学号'},
    )
    end_id = forms.IntegerField(
        required=True,
        label="End Id",
        error_messages={'required': '请输入末尾学号'},
    )
    password = forms.CharField(
        required=True,
        label="Password",
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(),
    )

class NewProfessor(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        error_messages={'required': '请输入用户名'},
    )
    password = forms.CharField(
        required=True,
        label='Password',
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(),
    )
    is_superuser = forms.BooleanField(
        required=False,
        label='Superuser',
    )