from django.contrib import admin
from.models import (CategoryBakerys,ItemBakerys,OrderBakerys,OrderItemBakerys,
                    CustomerBakerys,ItemChoicesBakerys,
                    ItemChoiceCategoryBakerys,IventoryItemCategoryBakerys,IventoryItemBakerys)


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','name','email')
admin.site.register(CustomerBakerys,CustomerAdmin)


class ItemChoicesAdmin(admin.ModelAdmin):
    list_display = ('parent_food','name','choice_category','prix','date_created')
admin.site.register(ItemChoicesBakerys,ItemChoicesAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(CategoryBakerys,CategoryAdmin)


class ItemChoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','date_created')
admin.site.register(ItemChoiceCategoryBakerys,ItemChoiceCategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','description', 'category','date_created','img')
admin.site.register(ItemBakerys,ItemAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','item','ingredient','seasoning','cuisson' ,'quantity','date_added')
admin.site.register(OrderItemBakerys,OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','table' ,'transaction_id','complete','status' ,'date_ordered','date_completed')
admin.site.register(OrderBakerys,OrderAdmin)

class IventoryItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','date_created')
admin.site.register(IventoryItemCategoryBakerys,IventoryItemCategoryAdmin)

class IventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name','prix','quantity' ,'category','description','date_created')
admin.site.register(IventoryItemBakerys,IventoryItemAdmin)


