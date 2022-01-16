from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from .forms import models
from.models import Item,ItemChoices,ItemChoiceCategory,IventoryItem
from django.contrib.auth.models import AbstractUser, User,AbstractBaseUser,BaseUserManager
from django.contrib.auth.forms import UserCreationForm, UsernameField
# from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import get_user_model



class CustomerForm(UserCreationForm):
   nom = forms.CharField(label = 'Nom')
   prenom = forms.CharField(label = 'Prenom')
   phone_number = forms.CharField(label = 'Phone Number')
   
   class Meta:
    model = User
    fields = ('username','phone_number','nom','prenom')
    
    
    
    
class ItemChoiceForm(forms.ModelForm):
   name = forms.ModelMultipleChoiceField(queryset=ItemChoices.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
   choice_category = forms.ModelMultipleChoiceField(queryset=ItemChoiceCategory.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
   class Meta:
      model = ItemChoices
      exclude=['parent_food','description','date_created','prix']
      
      
class AddProducts(forms.ModelForm):
   class Meta:
      model = IventoryItem
      exclude = ['date_created','description']
      
   

        
