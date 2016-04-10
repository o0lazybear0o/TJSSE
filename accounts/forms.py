from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from accounts.models import UserProfile, Credit
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
        error_messages={'required': '请输入姓氏'},
    )
    last_name = forms.CharField(
        required="True",
        error_messages={'required': '请输入名字'},
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangeStudentInfoForm(ModelForm):
    grade = forms.IntegerField(
        required="True",
        error_messages={'required': '请输入年级'},
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


class NewCreditForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(NewCreditForm, self).__init__(*args, **kwargs)
