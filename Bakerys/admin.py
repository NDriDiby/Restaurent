from django.contrib import admin
from .models import Category,ItemBakerys,OrderBakerys,OrderItemBakerys,CustomerBekerys

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(Category,CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','description', 'category','date_created','img')
admin.site.register(ItemBakerys,ItemAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','item','order','quantity','date_added')
admin.site.register(OrderItemBakerys,OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'table' ,'note','transaction_id','complete','status' ,'date_ordered','date_completed')
admin.site.register(OrderBakerys,OrderAdmin)


class CustomerBekerysAdmin(admin.ModelAdmin):
    list_display = ('user','name','email')
admin.site.register(CustomerBekerys,CustomerBekerysAdmin)

