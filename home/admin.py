from django.contrib import admin
from .models import *

# Register your models here.

class RentAdmin(admin.ModelAdmin):
    list_display = ['title','rent_per_day']


admin.site.register(RentItems,RentAdmin)
admin.site.register(RentOrder)



admin.site.site_header = 'Dream Nest Administration'