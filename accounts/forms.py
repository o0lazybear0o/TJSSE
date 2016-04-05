from django import forms
from accounts.models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="UserName",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class':"form-control",
                'placeholder':"UserName",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="Password",
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class':"form-control",
                'placeholder':"Password",
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()