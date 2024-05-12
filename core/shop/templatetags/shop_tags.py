from django import template
from shop.models import ProductStatusType, ProductModel, WishlistProductModel

register = template.Library()

@register.inclusion_tag('includes/latest-products.html', takes_context=True)
def show_latest_products(context):
    # get user request
    request = context.get('request')
    latest_products = ProductModel.objects.filter(status=ProductStatusType.publish.value).order_by('-created_date')[:8]
    wishlist_items = WishlistProductModel.objects.filter(user=request.user).values_list('product__id', flat=True) if request.user.is_authenticated else []
    return {"latest_products":latest_products, "request":request, 'wishlist_items':wishlist_items}

@register.inclusion_tag('includes/similar-products.html', takes_context=True)
def show_similar_products(context, product):
    request = context.get('request')
    product_categories = product.category.all()
    similar_products = ProductModel.objects.filter(status=ProductStatusType.publish.value,category__in=product_categories).distinct().exclude(id=product.id).order_by('-created_date')[:4]
    wishlist_items = WishlistProductModel.objects.filter(user=request.user).values_list('product__id', flat=True) if request.user.is_authenticated else []
    return {"similar_products":similar_products, "request":request, 'wishlist_items':wishlist_items} 


@register.inclusion_tag('includes/latest3-products.html')
def show_3_latest_products():
    latest3_products = ProductModel.objects.filter(status=ProductStatusType.publish.value).order_by('-created_date')[:6]
    return {"latest3_products":latest3_products}