from django import forms
from django.forms import ModelForm
from .models import Project
from  .models import ProjectType
import datetime

class SearchForm(forms.Form):

    DEFAULT_VAL=-1
    DEFAULT_TUPLE=(DEFAULT_VAL,'(无)')

    STATUS_TYPE_CHOICES=Project.STATUS_CHOICES[:]
    PROJ_TYPE_CHOICES=ProjectType.TYPE_CHOICES[:]
    STATUS_TYPE_CHOICES.insert(0,DEFAULT_TUPLE)
    PROJ_TYPE_CHOICES.insert(0,DEFAULT_TUPLE)

    status_type=forms.ChoiceField(
        choices=STATUS_TYPE_CHOICES,
        required=False,
        label='项目状态',
        initial=DEFAULT_TUPLE
    )
    project_type=forms.ChoiceField(
        choices=PROJ_TYPE_CHOICES,
        required=False,
        label='项目类型',
        initial=DEFAULT_TUPLE
    )

    search_val=forms.CharField(
        required=False,
        label='关键字'
    )

    search_date=forms.DateField(
        label='截止时间',
        required=False
    )

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

