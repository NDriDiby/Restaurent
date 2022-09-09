from unicodedata import category
from xmlrpc.client import Boolean
from django import forms
from django.db import models
from django.forms import BooleanField, ImageField, ModelForm
from django.db.models import fields
from django.db.models.fields import DateTimeField
from .forms import models
from.models import Accompagnement, Category, Item,ItemChoices,ItemChoiceCategory,IventoryItem, Supplement
from django.contrib.auth.models import AbstractUser, User,AbstractBaseUser,BaseUserManager
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import  TextInput, DateInput,NumberInput,DateTimeBaseInput,Textarea,Select,SelectMultiple



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
      

class AddSupplementForm(forms.ModelForm):
   class Meta:
      model = Supplement
      exclude = ['img','item']
      
   widgets = {
           'name': TextInput(attrs={'type': 'text','class':'form-control form-control-lg'}),
            'prix': NumberInput(attrs={'type': 'number','class':'form-control form-control-lg'}),
            }
      
      

class AddItem(forms.ModelForm):
   
   supplement = forms.ModelMultipleChoiceField(queryset=Supplement.objects.all(),required=False, 
                                               widget=forms.SelectMultiple(attrs={'type': 'text','class':'form-control form-control-lg'}))
   
   option_category = forms.ModelChoiceField(queryset= ItemChoiceCategory.objects.all(),required=False,
                                           widget=forms.Select(attrs={'type': 'option','class':'form-control form-control-lg category'}) )
   class Meta:
      model = Item
      exclude = ['itm_id']
      
      widgets = {
            'name': TextInput(attrs={'type': 'text','class':'form-control form-control-lg'}),
            'prix': NumberInput(attrs={'type': 'number','class':'form-control form-control-lg'}),
            'description':Textarea(attrs={'type': 'text','class':'form-control form-control-lg','rows':"2", 'cols':"3"}),
            'accompagnement': SelectMultiple(attrs={'type': 'text','class':'form-control form-control-lg'}),
            'category': Select(attrs={'type': 'option','class':'form-control form-control-lg category'}),
            }
      
class AddMenu(forms.ModelForm):
   
   class Meta:
      model = Category
      fields = ['name']
      
      widgets = {
            'name': TextInput(attrs={'type': 'text','class':'form-control form-control-lg cat'}),
           
        }
      
   
class AddAccompForm(forms.ModelForm):
   
   class Meta:
      model = Accompagnement
      fields = ['name','prix','img']
      
      widgets = {
            'name': TextInput(attrs={'type': 'text','class':'form-control form-control-lg'}),
             'prix': NumberInput(attrs={'type': 'number','class':'form-control form-control-lg'}),
        }



class AddOptionCategoryForm(forms.ModelForm):
   category_opt = forms.ModelChoiceField(queryset = ItemChoiceCategory.objects.all(),
                                     widget=Select(attrs={'type': 'text','class':'form-control form-control-lg'}),)
   class Meta: 
      model = ItemChoiceCategory
      fields = ['name', 'category_opt' ,'item','multiple_choice']
      
      
      widgets = {
               'name': TextInput(attrs={'type': 'text','class':'form-control form-control-lg'}),
               'item': SelectMultiple(attrs={'type': 'text','class':'form-control form-control-lg'}),
               # 'category': Select(attrs={'type': 'text','class':'form-control form-control-lg'}),
               }
   

class AddOptionForm(forms.ModelForm):
   choice = forms.ModelChoiceField(queryset = ItemChoices.objects.all(),
                                     widget=Select(attrs={'type': 'text','class':'form-control form-control-lg'}),)
   class Meta: 
      model = ItemChoices
      exclude =['prix','description']
      
      widgets = {
               'name': TextInput(attrs={'type': 'text','class':'form-control form-control-lg'}),
               'choice_category':Select(attrs={'type': 'text','class':'form-control form-control-lg',}),
               'parent_food': SelectMultiple(attrs={'type': 'text','class':'form-control form-control-lg'}),
               }
      
   
