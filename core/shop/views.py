from django.shortcuts import render
from django.views.generic import (
    View,
    ListView,
    DetailView,
)
from .models import ProductModel, ProductStatusType, ProductCategoryModel, WishlistProductModel
from django.core.exceptions import FieldError
from website.models import NewsLetterModel
from website.forms import NewsLetterForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from cart.models import CartModel
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
        # wishlist and  get only product id
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list('product__id', flat=True)
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
        # wishlist and  get only product id
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list('product__id', flat=True)
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    

class ShopProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            cart, created = CartModel.objects.get_or_create(user=user)
            cart_item = cart.cart_items.filter(product=product).first()
            context['product_quantity'] = cart_item.quantity if cart_item else 0
            context['product_price'] = product.get_price() 
                        # wishlist and  get only product id
            context["is_wished"] = WishlistProductModel.objects.filter(user=self.request.user, product__id=self.get_object().id).exists()
            context['total_product_price'] = context['product_quantity'] * context['product_price']
        else:
            context['product_quantity'] = 0
            context['product_price'] = product.get_price()
            context['total_product_price'] = 0
        return context
     
class NewsLetterView(View):
    http_method_names = ['post']
    model = NewsLetterModel()
    form_class = NewsLetterForm

    def post(self, request):
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            # Process the form data
            email = form.cleaned_data['email']
            # Save the form data or perform any desired actions
            form.save()
            messages.add_message(request,messages.SUCCESS,'your ticket submitted successfully')  # Redirect to a success page
            return redirect(self.get_success_url())
        else:
            messages.add_message(request,messages.ERROR,'your ticket didnt submitted')
            return redirect('shop:product-grid')
    
    def get_success_url(self):
        return reverse_lazy('shop:product-grid')