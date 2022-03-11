from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from .forms import models
from.models import Category, Item,ItemChoices,ItemChoiceCategory,IventoryItem
from django.contrib.auth.models import AbstractUser, User,AbstractBaseUser,BaseUserManager
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class CustomerForm(UserCreationForm):
   

   nom = forms.CharField(label = 'Nom')
   prenom = forms.CharField(label = 'Prenom')
   phone_number = forms.CharField(label = 'Phone Number')
   
   
   class Meta:
    model = User
    fields = ['username','phone_number','nom','prenom']

    labels = {
            'username': _('Email'),
         }
    error_messages={
       'phone_number':{
          'required': _("You need an email bro")
       }
    }
    
    
    
   def clean_username(self):
      email = self.cleaned_data.get('username')
      allUser= User.objects.values_list('username',flat=True)
      
      
      if email in allUser:
         raise forms.ValidationError(f"{email} exist deja. Veuillez choisir une autre addresse e-mail.")
      
      elif "@" not in email:
         raise forms.ValidationError(f"Veillez entrez une adresse e-mail valide.")
      
      return email
   
   def clean_password2(self):
      
      password1 = self.cleaned_data.get('password1')
      password2 = self.cleaned_data.get("password2")
        
      if len(password1) < 8:
         raise forms.ValidationError("Ce mot de passe est trop court. Il doit contenir au moins 8 caractères.")
      
      elif password1 and password2 and password1 != password2:
            raise ValidationError("Les deux champs de mot de passe ne correspondent pas.")
         
      return password2
    
   def clean_phone_number(self):
      phone = self.cleaned_data.get('phone_number')
      
      if not phone.startswith("+225"):
         print(phone)
         raise forms.ValidationError("Veillez entrer votre numero de telephone avec +225")
      return phone
      
    
    
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
      

class AddItem(forms.ModelForm):
   class Meta:
      model = Item
      exclude = ['itm_id']
      
class AddMenu(forms.ModelForm):
   
   class Meta:
      model = Category
      exclude = ['cat_id','date_created']
      
   

        
