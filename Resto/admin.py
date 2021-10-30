from django.contrib import admin
from.models import Category,Item

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(Category,CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','description', 'category','date_created')
admin.site.register(Item,ItemAdmin)