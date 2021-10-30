
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Category(models.Model):
    cat_id = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100,blank=True)
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
    date_created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=CASCADE)


    def __str__(self):
        return self.name
    