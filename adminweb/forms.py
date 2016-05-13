from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile, Credit
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


class SuperEditProjectForm(forms.Form):
    project_status = forms.ChoiceField(
        choices=Project.STATUS_CHOICES,
        label='Project Status',
        required=True,
        error_messages={'required': '请输入项目状态'},
    )


class SuperEditCreditForm(forms.Form):
    credit_type = forms.ChoiceField(
        choices=Credit.CREDIT_TYPE_CHOICES,
        label='credit_type',
        required=True,
        widget=forms.Select(attrs={'class': 'credit_type'}),
        error_messages={'required': '请输入学分类型1'},
    )
    credit_second_type = forms.ChoiceField(
        choices=Credit.CREDIT_SECOND_TYPE,
        label='credit_type',
        required=True,
        widget=forms.Select(attrs={'class': 'credit_second_type'}),
        error_messages={'required': '请输入学分类型2'},
    )
    credit_third_type = forms.ChoiceField(
        choices=Credit.CREDIT_THIRD_TYPE,
        label='credit_type',
        required=True,
        widget=forms.Select(attrs={'class': 'credit_third_type'}),
        error_messages={'required': '请输入学分类型3'},
    )

    get_project_date = forms.DateTimeField(
        required=True,
        label="Get Project Date",
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        error_messages={'required': '请输入获得奖项时间'},
    )
    credit_name = forms.CharField(
        required=True,
        label="Credit Name",
        error_messages={'required': '请输入学分名称'},
    )
    status = forms.ChoiceField(
        required=True,
        choices=Credit.CREDIT_STATUS_CHOICES,
        label="Status",
        error_messages={'required': '请输入学分状态'},
    )
    value = forms.IntegerField(
        required=True,
        label="Value",
        error_messages={'required': '请输入学分大小'},
    )
    grade = forms.ChoiceField(
        required=True,
        choices=Credit.CREDIT_GRADE,
        label="Grade",
        error_messages={'required': '请输入学分成绩'},
    )

    def __init__(self, *args, **kwargs):
        super(SuperEditCreditForm, self).__init__(*args, **kwargs)