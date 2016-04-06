from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile
from django.contrib.auth.models import User
from project.models import Project, ProjectType


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
        required=True,
        label="New Password Again",
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()


class NewProjectForm(forms.Form):
    project_type = forms.ModelChoiceField(
        queryset=None,
        required=True,
        label='Project Type',
        error_messages={'required': '请选择项目类型'}
    )
    project_name = forms.CharField(
        required=True,
        label="Project Name",
        error_messages={'required': '请输入项目名称'},
    )
    professor = forms.ModelChoiceField(
        queryset=None,
        required=True,
        label='Professor',
        error_messages={'required': '请选择导师'})
    partner1 = forms.CharField(
        required=False,
        label="Partner ID (Optional)",
    )
    partner2 = forms.CharField(
        required=False,
        label="Partner ID (Optional)",
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(
        ),
    )

    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)
        self.fields['professor'].queryset = UserProfile.objects.filter(type=UserProfile.TYPE_PROFESSOR)
        self.fields['project_type'].queryset = ProjectType.objects.filter(isopening=True)
