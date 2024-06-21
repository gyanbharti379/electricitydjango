from django.contrib import admin
from .models import Customer,MeterInfo,ServiceCharge,tax,bill

# Register your models here.
admin.site.register(Customer)
admin.site.register(MeterInfo)
admin.site.register(ServiceCharge)
admin.site.register(tax)
admin.site.register(bill)
