from django.contrib import admin
from .models import ProductModel, ProductCategoryModel, ProductImageModel
# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "stock", "status", "price", "created_date")

class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")


class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")


admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(ProductCategoryModel, ProductCategoryModelAdmin)
admin.site.register(ProductImageModel, ProductImageModelAdmin)
