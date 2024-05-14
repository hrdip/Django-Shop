from django.db import models
from shop.models import ProductModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
# Create your models here.

class ReviewStatusType(models.IntegerChoices):
    pending = 1 ,("در انتظار تایید")
    accepted = 2 ,("تایید شده ")
    rejected = 3 ,("رد شده ")


class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user} - {self.product.title}"

    class Meta:
        ordering = ['-created_date']
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate the average rating for the product
        avg_rating = ReviewModel.objects.filter(product=self.product).aggregate(Avg('rate'))['rate__avg']
        self.product.avg_rate = avg_rating or 0  # Set to 0 if no reviews yet
        self.product.save()

# active when ReviewModel active and create revie
@receiver(post_save, sender=ReviewModel)
def calculate_avg_review(sender, instance, created, **kwargs):
    pass
