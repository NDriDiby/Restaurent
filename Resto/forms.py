from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from django import forms
from.models import Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CustomerForm(UserCreationForm):
   table = forms.IntegerField(label = 'Table Number')
   phone_number = forms.CharField(label = 'Phone Number')

   class Meta:
    model = User
    fields = ('username','table','phone_number')
        
