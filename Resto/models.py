
from ast import AugLoad
from datetime import datetime
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser,User,AbstractBaseUser,BaseUserManager,PermissionsMixin
# from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings

from PIL import Image
from pathlib import Path
from django_resized import ResizedImageField



#Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100,blank=True)
    img = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = 'Categorie'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=10,null=True, blank=True,default=1)
    

    def __str__(self):
        return self.name
    
    
    def full_name(self):
        
        return self.user.get_full_name()
    

class Accompagnement(models.Model):
    name = models.CharField(max_length = 150)
    prix = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0,blank=True)
    img = models.ImageField(upload_to='images/')
    
    
    def __str__(self):
        return self.name
    

 
class Item(models.Model):
    name = models.CharField(max_length = 150)
    prix = models.IntegerField()
    description = models.TextField(max_length=150,blank=True)
    img = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=CASCADE)
    accompagnement = models.ManyToManyField(Accompagnement,blank=True)
   
   

    def __str__(self):
        return self.name
    

class ItemChoiceCategory(models.Model):
    name = models.CharField(max_length = 50,blank=True)
    item = models.ManyToManyField(Item,blank=True)
    multiple_choice = models.BooleanField(default=False,blank=True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class ItemChoices(models.Model):
    name = models.CharField(max_length = 150,blank=True)
    choice_category = models.ForeignKey(ItemChoiceCategory,on_delete=models.CASCADE,blank=True,null=True)
    parent_food = models.ManyToManyField(Item,blank=True)
    description = models.TextField(max_length=20,blank=True)
    prix = models.IntegerField(blank=True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    transaction_id = models.CharField(null = True, blank = True,max_length=20)
    complete = models.BooleanField(default=False,null=True,blank=False)
    status = models.CharField(max_length=20,default = 'Pending')
    date_ordered = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(auto_now_add=True)
    table = models.IntegerField(default=1)
    
    class meta:
        permissions = [("view order","can view order")]

    def __str__(self):
        return str(self.customer)
    
    
    #Total value of cart
    def get_order_total(self):
        order_item = self.orderitem_set.all()
        total = sum([item.get_total() for item in order_item])
        if self.sideorderitem_set.all():
            side_item = self.sideorderitem_set.all()
            total_side = sum([item.total_side_order() for item in side_item])
            return total + total_side
        else:
            return total


    #Total quantity in the cart
    def get_order_quantity(self):
        order_item = self.orderitem_set.all()
        total = sum([item.quantity for item in order_item])
        if self.sideorderitem_set.all():
            side_item = self.sideorderitem_set.all()
            total_side = sum([item.quantity for item in side_item])
            return total + total_side
        else:
            return total
        
    def total_side_order_item(self):
        side = self.sideorderitem_set.all()
        total = sum([x.quantity for x in side])
        return total
    
    
class Supplement(models.Model):
    name = models.CharField(max_length = 150)
    prix = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0,blank=True)
    item = models.ManyToManyField(Item,blank = True)
    img = models.ImageField(upload_to='images/',blank = True)
    
    def __str__(self):
        return self.name
    
    

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    item = models.ForeignKey(Item, on_delete=CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0,null = True, blank = True )
    ingredient = models.CharField(null = True, blank = True,max_length=150)
    accompagnememt = models.ManyToManyField(Accompagnement,blank=True)
    supplement = models.ManyToManyField(Supplement,blank=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item)
    
    def total_supplement(self):
        if self.supplement:
            all_sup = self.supplement.all()
            total_sup = sum([x.prix for x in all_sup])
            return total_sup
        return 0
    
    
    def total_ind_sup(self):
        if self.supplement:
            total = self.quantity * self.supplement.prix
            return total
    
    #Get total
    def get_total(self):
        total = (self.item.prix * self.quantity) 
        sup = self.total_supplement()
        global_total = total + sup
        if sup!=0:
            sup = self.quantity * self.total_supplement()
            global_total = total + sup
        return global_total 
    
    
    def get_total_item(self):
        total = (self.item.prix * self.quantity)
        return total
    
    def get_total_accomp(self):
        total = self.quantity * self.total_supplement()
        return total
    
    
class SideOrderItem(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    item = models.ForeignKey(Accompagnement, on_delete=CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0,null = True, blank = True )
    date_added = models.DateTimeField(auto_now=True,)
    img = models.ImageField(upload_to='images/',blank = True)
    
    def __str__(self):
        return str(self.item)
    
    
    def total_side_order(self):
        total = (self.item.prix) * (self.quantity)
        return total
    
    
class IventoryItemCategory(models.Model):
    name = models.CharField(max_length=150,null = True, blank = True)
    description = models.CharField(max_length=150,null = True, blank = True)
    date_created = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return self.name
    
    def total_spending_category(self):
        category = self.iventoryitem_set.all()
        spending = sum([item.prix for item in category])
        return spending
    
    def total_item_category(self):
        category = self.iventoryitem_set.all()
        count = len([item.name for item in category])
        return count
        
    
class IventoryItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150,null = True, blank = True)
    date_created = models.DateTimeField(auto_now=True)
    prix = models.IntegerField(blank=True)
    quantity = models.IntegerField(blank=True)
    category = models.ForeignKey(IventoryItemCategory,on_delete=CASCADE,blank=True,null=True)
    date_created = models.DateTimeField(auto_now=True)
    
    class meta:
        permissions = [("view iventory item ","can view iventory item")]
        
    def __str__(self):
        return self.name
    

class Transactions(models.Model):
    
    user = models.ForeignKey(Customer,verbose_name='customer',on_delete=models.CASCADE)
    amount= models.CharField(max_length=150,blank=True)
    currency= models.CharField(max_length=150,blank=True)
    description= models.CharField(max_length=150,blank=True)
    operator_id= models.CharField(max_length=150,blank=True)
    payment_date= models.CharField(max_length=150,blank=True)
    payment_method= models.CharField(max_length=150,blank=True)
    status= models.CharField(max_length=150,blank=True)
    transactionID = models.CharField(max_length=150,blank=True,primary_key=True)
    # order = models.ForeignKey(Order,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name_plural = "Transactions"
    

