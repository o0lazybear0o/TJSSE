import django
from .models import News
from django import forms

class SearchForm(forms.Form):

    search_val=forms.CharField(
        required=False,
        label='关键字'
    )
