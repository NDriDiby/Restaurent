from django.contrib import admin
from.models import Category,Item,Order,OrderItem,Customer,ItemChoices,Accompagment

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','name','email')
admin.site.register(Customer,CustomerAdmin)


class ItemChoicesAdmin(admin.ModelAdmin):
    list_display = ('parent_food','name','description','prix','date_created')
admin.site.register(ItemChoices,ItemChoicesAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(Category,CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','description', 'category','date_created','img')
admin.site.register(Item,ItemAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','item','item_choice' ,'order','quantity','date_added')
admin.site.register(OrderItem,OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','table' ,'transaction_id','complete','status' ,'date_ordered','date_completed')
admin.site.register(Order,OrderAdmin)