from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from django import forms
from.models import OrderBakerys
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class OrderForm(forms.ModelForm):
   
   class Meta:
    model = OrderBakerys
    fields = ('note',)
        
