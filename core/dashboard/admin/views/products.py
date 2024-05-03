from django.views.generic import  TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm, ProductForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
from shop.models import ProductModel, ProductCategoryModel, ProductStatusType
from django.core.exceptions import FieldError
# Create your views here.

class AdminProductListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = 'dashboard/admin/products/product-list.html'
    paginate_by = 10 

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    # filters and get response
    def get_queryset(self):
        queryset = ProductModel.objects.all()
        
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
    

class AdminProductEditView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    
    template_name = 'dashboard/admin/products/product-edit.html'
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "product was successfully updated"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-detail", kwargs={"pk",self.get_object().pk})