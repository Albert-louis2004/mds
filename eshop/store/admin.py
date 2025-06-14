# shop/admin.py

from django.contrib import admin
from .models import Manufacturer, Memory, SSD, Processor, Laptop

class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'memory_list', 'ssd_list', 'processor', 'price', 'quantity')
    search_fields = ('name', 'manufacturer', 'processor')
    list_filter = ('memory', 'ssd', 'processor', 'manufacturer')

    def memory_list(self, obj):
        return ", ".join([mem.size for mem in obj.memory.all()])
    memory_list.short_description = 'Memory'

    def ssd_list(self, obj):
        return ", ".join([ssd.size for ssd in obj.ssd.all()])
    ssd_list.short_description = 'SSD'

admin.site.register(Manufacturer)
admin.site.register(Memory)
admin.site.register(SSD)
admin.site.register(Processor)
admin.site.register(Laptop, LaptopAdmin)  # Register Laptop with LaptopAdmin
