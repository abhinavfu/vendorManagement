from django.contrib import admin
from .models import Vendor, Purchase_Order, Historical_Performance
# Register your models here.

# admin.site.register((Vendor, Purchase_Order, Historical_Performance))

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'vendor_code','on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


@admin.register(Purchase_Order)
class Purchase_OrderAdmin(admin.ModelAdmin):
    list_display = ['id','po_number', 'vendor','status','order_date','delivery_date','quality_rating','issue_date', 'acknowledgment_date']


@admin.register(Historical_Performance)
class Historical_PerformanceAdmin(admin.ModelAdmin):
    list_display = ['id','vendor','on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate', 'date']