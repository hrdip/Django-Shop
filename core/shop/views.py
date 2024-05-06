from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import ProductModel, ProductStatusType, ProductCategoryModel
from django.core.exceptions import FieldError
from cart.cart import CartSession
# Create your views here.

class ShopProductGridView(ListView):
    template_name = 'shop/product-grid.html'
    paginate_by = 9 

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    # filters and get response
    def get_queryset(self):
        queryset = ProductModel.objects.filter(
            status=ProductStatusType.publish.value)
        
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
        

class ShopProductListView(ListView):
    template_name = 'shop/product-list.html'
    paginate_by = 9 

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    # filters and get response
    def get_queryset(self):
        queryset = ProductModel.objects.filter(
            status=ProductStatusType.publish.value)
        
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    

class ShopProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        product = self.get_object()
        cart_item = None
        for item in cart.get_cart_dict()["items"]:
            if item["product_id"] == str(product.id):
                cart_item = item
                break
        
        if cart_item is not None:
            context['product_quantity'] = cart_item["quantity"]
        else:
            context['product_quantity'] = 0
        return context
     