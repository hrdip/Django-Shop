from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from shop.models import WishlistProductModel
from django.shortcuts import redirect
from django.core.exceptions import FieldError
# Create your views here.


class CustomerWishlistListView(HasCustomerAccessPermission, LoginRequiredMixin, ListView):
    template_name = 'dashboard/customer/wishlists/customer-wishlist-list.html'
    paginate_by = 5

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    # filters and get response
    def get_queryset(self):
        queryset = WishlistProductModel.objects.filter(user=self.request.user)
        
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(product__title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = self.get_queryset().count()
        return context
 

class CustomerWishlistDeleteView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    http_method_names = ['post']
    success_message = "wishlist was successfully deleted"
    success_url = reverse_lazy("dashboard:customer:customer-wishlist-list")
    
    def get_queryset(self):
        return WishlistProductModel.objects.filter(user=self.request.user)

