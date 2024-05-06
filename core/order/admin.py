from django.contrib import admin
from .models import OrderModel, OrderItemModel, UserAddresModel, CouponModel 
# Register your models here.

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "coupon", "status", "created_date")

class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price", "created_date")


class UserAddresModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "address", "state", "city", "zip_code", "created_date")

class CouponModelAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "discount_percent", "max_limit_usage",  "expiration_date", "used_by_count", "created_date")
    
    def used_by_count(self,obj):
        return obj.used_by.all().count()

admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderItemModel, OrderItemModelAdmin)
admin.site.register(UserAddresModel, UserAddresModelAdmin)
admin.site.register(CouponModel, CouponModelAdmin)