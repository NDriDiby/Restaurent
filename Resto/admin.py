from django.contrib import admin
from.models import (Category,Item,Order,OrderItem,
                    Customer,ItemChoices,
                    ItemChoiceCategory,IventoryItemCategory,IventoryItem)


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','name','email','phone')
admin.site.register(Customer,CustomerAdmin)


class ItemChoicesAdmin(admin.ModelAdmin):
    list_display = ('parent_food','name','choice_category','prix','date_created')
admin.site.register(ItemChoices,ItemChoicesAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(Category,CategoryAdmin)


class ItemChoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','date_created')
admin.site.register(ItemChoiceCategory,ItemChoiceCategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','description' ,'category','date_created','img')
admin.site.register(Item,ItemAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','item','ingredient','seasoning','cuisson' ,'quantity','date_added')
admin.site.register(OrderItem,OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','table' ,'transaction_id','complete','status' ,'date_ordered','date_completed')
admin.site.register(Order,OrderAdmin)

class IventoryItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(IventoryItemCategory,IventoryItemCategoryAdmin)

class IventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','quantity','category','description','date_created')
admin.site.register(IventoryItem,IventoryItemAdmin)

# class AccompagementAdmin(admin.ModelAdmin):
#     list_display = ('name','prix')
# admin.site.register(Accompagnement,AccompagementAdmin)


