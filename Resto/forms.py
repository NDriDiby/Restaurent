from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from django import forms
from.models import Item



class ItemOrder(ModelForm):
    table = models.IntegerField()
    date_created = DateTimeField(auto_now=True)

    class Meta:
        model = Item
        fields = ['name','prix']
        

