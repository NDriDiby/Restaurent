from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import  TextInput, DateInput,NumberInput,DateTimeBaseInput,Textarea,Select,SelectMultiple


class LoginForm (forms.Form):
    
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    class Meta:
      
        widgets = {
           'username': TextInput(attrs={'type': 'text','class':'form-control form-control-lg'}),
            'password': TextInput(attrs={'type': 'password','class':'form-control form-control-lg'}),
            }