from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import ProductModel, ProductStatusType
# Create your views here.

class ShopProductGridView(ListView):
    template_name = 'shop/product-grid.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

class ShopProductListView(TemplateView):
    template_name = 'shop/product-list.html'