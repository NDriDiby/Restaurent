
from ast import AugLoad
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import Permission, User


steak_choice = [('Rare','Rare'),
                ('Medium','Medium'),
                ('Medium Rare','Medium Rare'),
                 ('Medium Well','Medium Well'),
                ('Well Done','Well Done')]


coca_cola_product = [('Coca-Cola','Coca-Cola'),
                     ('Fanta','Fanta'),
                     ('Sprite','Sprite')]


assaisonement = [('Avec Piment','Avec Piment'),
                 ('Sans Piment','Sans Piment')]



# Create your models here.
class Category(models.Model):
    cat_id = models.IntegerField()
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

    def __str__(self):
        return self.name



class Item(models.Model):
    itm_id = models.IntegerField()
    name = models.CharField(max_length = 150)
    prix = models.IntegerField()
    description = models.TextField(max_length=150,blank=True)
    img = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=CASCADE)
    assaisonement = models.CharField(max_length = 50, choices=assaisonement,blank = True)
    steak_choice = models.CharField(max_length = 50,choices=steak_choice,blank=True)
    boisson_choice = models.CharField(max_length = 50,choices=coca_cola_product,blank=True)


    def __str__(self):
        return self.name
    

class Accompagment(models.Model):
    pass

class ItemChoices(models.Model):
    parent_food = models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length = 150,blank=True)
    description = models.TextField(max_length=150,blank=True)
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
    date_completed = models.DateTimeField(auto_now=True)
    table = models.IntegerField(default=1)
    note = models.TextField(blank=True,max_length=50)

    class meta:
        permissions = (("can view orders"))

    def __str__(self):
        return str(self.customer.name)

    #Total value of cart
    def get_order_total(self):
        order = self.orderitem_set.all()
        total = sum([item.get_total() for item in order])
        return total


    #Total quantity in the cart
    def get_order_quantity(self):
        order = self.orderitem_set.all()
        total = sum([item.quantity for item in order])
        return total

    
class OrderItem(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    item = models.ForeignKey(Item, on_delete=CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=0,null = True, blank = True )
    item_choice = models.ForeignKey(ItemChoices,on_delete=models.CASCADE,blank=True,null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item)

    #Get total
    def get_total(self):
        total = self.item.prix * self.quantity
        return total



