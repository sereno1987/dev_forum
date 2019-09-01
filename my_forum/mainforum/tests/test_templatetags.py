from django import forms
from django.test import testcases
from ..templatetags.form_tags import input_class, field_type

class FormExample(forms.Form):
    text=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields=('text', 'password')

