from django.contrib import admin
from .models import ProductModel, ProductCategoryModel, ProductImageModel, WishlistProductModel
# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "stock", "status", "price", "discount_pecent", "created_date")

class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")


class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")


class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_date")


admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(ProductCategoryModel, ProductCategoryModelAdmin)
admin.site.register(ProductImageModel, ProductImageModelAdmin)
admin.site.register(WishlistProductModel, WishlistProductModelAdmin)
