from django.contrib import admin

from .models import phone

class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id','numb')
admin.site.register(phone,PhoneAdmin)

# Register your models here.
