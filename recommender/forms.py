from django import forms
from .models import *

class EnterProfInfo(forms.Form):
    prof_name = forms.CharField(label='Name of researcher', max_length=500)
    topics = forms.CharField(label="Topics")