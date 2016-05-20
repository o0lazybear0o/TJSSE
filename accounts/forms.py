from django import forms
from django.forms import ModelForm
from django.forms.extras import widgets
from accounts.models import UserProfile, Credit
from django.contrib.auth.models import User
from project.models import Project, ProjectType, Fund


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="用户名",
        error_messages={'required': '请输入用户名'},
    )
    password = forms.CharField(
        required=True,
        label="密码",
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()


class ChangeUserInfoForm(ModelForm):
    first_name = forms.CharField(
        required="True",
        label="姓",
        error_messages={'required': '请输入姓氏'},
    )
    last_name = forms.CharField(
        required="True",
        label="名",
        error_messages={'required': '请输入名字'},
    )
    email = forms.CharField(
        required="True",
        label="邮箱",
        error_messages={'required': '请输入邮箱'},
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': "姓",
            'last_name': "名",
            'email': "邮箱",
        }


class ChangeStudentInfoForm(ModelForm):
    grade = forms.IntegerField(
        required="True",
        label="年级",
        error_messages={'required': '请输入年级'},
    )

    class Meta:
        model = UserProfile
        exclude = ['user', 'type']
        labels = {
            'major': '专业方向',
            'phone': '电话',
        }


class ChangeProfessorInfoForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']
        labels = {
            'phone': "电话",
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        label="原密码",
        error_messages={'required': '请输入旧密码'},
        widget=forms.PasswordInput(),
    )
    new_password = forms.CharField(
        required=True,
        label="新密码",
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(),
    )
    new_password_again = forms.CharField(
        required=True,
        label="再次输入新密码",
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()


class NewProjectForm(forms.Form):
    project_type = forms.ModelChoiceField(
        queryset=ProjectType.objects.filter(isopening=True),
        required=True,
        label='项目类型',
        error_messages={'required': '请选择项目类型'}
    )
    project_name = forms.CharField(
        required=True,
        label="项目名称",
        error_messages={'required': '请输入项目名称'},
    )
    professor = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(type=UserProfile.TYPE_PROFESSOR),
        required=True,
        label='指导教师',
        error_messages={'required': '请选择导师'}
    )
    partner1 = forms.CharField(
        required=False,
        label="成员学号(可选)",
    )
    partner2 = forms.CharField(
        required=False,
        label="成员学号(可选)",
    )
    partner3 = forms.CharField(
        required=False,
        label="成员学号(可选)",
    )
    partner4 = forms.CharField(
        required=False,
        label="成员学号(可选)",
    )
    description = forms.CharField(
        required=False,
        label="项目描述",
        widget=forms.Textarea(
        ),
    )


class FundForm(ModelForm):
    class Meta:
        model = Fund
        fields = ['fund_type', 'value', 'note']
        labels = {
            'fund_type': '经费类型',
            'value': '经费',
            'note': '注释',
        }

# class NewCreditFrom(ModelForm):
#     class Meta:
#         model = Credit
#         fields = ['credit_type', 'credit_second_type', 'credit_third_type', 'get_project_date', 'credit_name', 'image']

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
    image = forms.ImageField(
        required=False,
        label="Image",
        # error_messages={'required': '请上传图片'}
    )

    def __init__(self, *args, **kwargs):
        super(NewCreditForm, self).__init__(*args, **kwargs)


# class ContactSearchForm(forms.Form):
#     content = forms.CharField(
#         required=False,
#         label="CONTENT",
#     )
#     grade = forms.ChoiceField(
#         # choices=Credit.CREDIT_TYPE_CHOICES,
#         label='GRADE',
#         required=True,
#     )
#
#     def clean(self):
#         cleaned_data = super(ContactSearchForm, self).clean()
