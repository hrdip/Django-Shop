from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class OrderStatusType(models.IntegerChoices):
    pending = 1, ("در انتظار پرداخت")
    processing = 2, ("در حال پرداخت")
    shipped = 3, (" ارسال شده")
    delivered = 4, ("تحویل داده شده")
    canceled = 5, ("لغو شده")

class UserAddressModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class CouponModel(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_percent = models.IntegerField(default=0, validators = [MinValueValidator(0),MaxValueValidator(100)])
    max_limit_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField('accounts.User', blank=True, null=True, related_name="coupon_users")
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class OrderModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    
    # order address informations
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    status = models.IntegerField(choices=OrderStatusType.choices, default=OrderStatusType.pending.value)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    coupon = models.ForeignKey(CouponModel, on_delete=models.PROTECT, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())

    def calculate_total_tax_price(self):
        return round(self.calculate_total_price()+((self.calculate_total_price() * 9)/100))
    
    def __str__(self):
        return f"{self.user.email}-{self.id}"
 
class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey("shop.ProductModel", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    

