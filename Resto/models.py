
from ast import AugLoad
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

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


class Item(models.Model):
    itm_id = models.IntegerField()
    name = models.CharField(max_length = 150)
    prix = models.FloatField()
    description = models.TextField(max_length=150,blank=True)
    img = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=CASCADE)


    def __str__(self):
        return self.name


class Order(models.Model):
    transaction_id = models.IntegerField()
    complete = models.BooleanField(default=False,null=True,blank=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.transaction_id)

    #Total value of cart
    def get_order_total(self):
        order = self.orderitem_set.all()
        total = sum([item.get_total() for item in order])
        return total


    def get_order_quantity(self):
        order = self.orderitem_set.all()
        total = sum([item.quantity for item in order])
        return total

    



class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=CASCADE, blank=True)
    order = models.ForeignKey(Order,on_delete=CASCADE, blank = True)
    quantity = models.IntegerField(default=0,null = True, blank = True )
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item)

    #Get total
    def get_total(self):
        total = self.item.prix * self.quantity
        return total