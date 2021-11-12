from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import Permission, User

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


class CustomerBekerys(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return self.name



class ItemBakerys(models.Model):
    itm_id = models.IntegerField()
    name = models.CharField(max_length = 150)
    prix = models.IntegerField()
    description = models.TextField(max_length=150,blank=True)
    img = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=CASCADE)


    def __str__(self):
        return self.name


class OrderBakerys(models.Model):
    customer = models.ForeignKey(CustomerBekerys,on_delete=models.SET_NULL,blank=True,null=True)
    transaction_id = models.IntegerField(default=0,null = True, blank = True )
    complete = models.BooleanField(default=False,null=True,blank=False)
    status = models.CharField(max_length=30,default = 'Pending')
    date_ordered = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(auto_now=True)

    class meta:
        permissions = (("can view orders"))

    def __str__(self):
        return str(self.customer.name)

    #Total value of cart
    def get_order_total(self):
        order = self.orderitembakerys_set.all()
        total = sum([item.get_total() for item in order])
        return total


    #Total quantity in the cart
    def get_order_quantity(self):
        order = self.orderitembakerys_set.all()
        total = sum([item.quantity for item in order])
        return total

    
class OrderItemBakerys(models.Model):
    customer = models.ForeignKey(CustomerBekerys,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(OrderBakerys,on_delete=models.SET_NULL,blank=True,null=True)
    item = models.ForeignKey(ItemBakerys, on_delete=CASCADE)
    order = models.ForeignKey(OrderBakerys,on_delete=CASCADE)
    quantity = models.IntegerField(default=0,null = True, blank = True )
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item)

    #Get total
    def get_total(self):
        total = self.item.prix * self.quantity
        return total



