
from django.db import models

# Create your models here.

class Category(models.Model):
    cat_id = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200,blank=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categories'

    def __str__(self):
        return self.name
