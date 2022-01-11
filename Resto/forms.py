from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from .forms import models
from.models import Item,ItemChoices,ItemChoiceCategory,IventoryItem
from django.contrib.auth.models import AbstractUser, User,AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _




   
class CustomerForm(UserCreationForm):
   nom = forms.CharField(label = 'Nom')
   prenom = forms.CharField(label = 'Prenom')
   email = forms.EmailField(label = 'Email')
   phone_number = forms.CharField(label = 'Phone Number')
   
   # error_messages = {
   #      'password_mismatch': _("The two password fields didn't match."),
   #  }
   
   # username = forms.CharField(label=_("Username"),
   #      help_text=_("Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."))
   
   # password1 = forms.CharField(label=_("Password"),
   #      widget=forms.PasswordInput)
  

   # password2 = forms.CharField(label=_("Password confirmation"),
   #      widget=forms.PasswordInput,
   #      help_text=_("Entrez le même password, pour verification."))
   

   class Meta:
    model = User
    fields = ('username','phone_number','nom','prenom','email')
    
    
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
      
   

        
