from typing import Any
from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField

# Create your models here.
class ProductStatusType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")

class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    # allow_unicode for multilanguage
    slug = models.SlugField(allow_unicode=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
 
    def __str__(self):
        return self.title

class ProductModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(default="/default/product-image.png", upload_to="product/img/")
    description = RichTextField()
    brief_description = RichTextField()
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_pecent = models.IntegerField(default=0, validators = [MinValueValidator(0),MaxValueValidator(100)])
    avg_rate = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title
    
    def get_price(self):
        return round(self.price - (self.price*Decimal(self.discount_pecent/100)))
    
    def get_show_price(self):
        return '{:,}'.format(round(self.price - (self.price*Decimal(self.discount_pecent/100))))

    def get_show_raw_price(self):
        return '{:,}'.format(self.price)

    def is_discounted(self):
        return self.discount_pecent != 0
    
    def is_published(self):
        return self.status == ProductStatusType.publish.value
    


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name="product_images")
    file = models.ImageField( upload_to="product/extra-img/")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self, *args: Any, **kwargs):
        return self.product.title



