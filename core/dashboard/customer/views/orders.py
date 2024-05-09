from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from order.models import OrderModel, OrderStatusType
from django.core.exceptions import FieldError
# Create your views here.


class CustomerOrderListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = 'dashboard/customer/orders/order-list.html'
    paginate_by = 5

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = OrderModel.objects.filter(user=self.request.user)
        
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(id__icontains=search_q)

        if status := self.request.GET.get("status"):
            queryset = queryset.filter(status=status)

        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = self.get_queryset().count()
        context["status_types"] = OrderStatusType.choices  
        return context

class CustomerOrderDetailView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    template_name = 'dashboard/customer/orders/order-detail.html'

    def get_queryset(self):
        queryset = OrderModel.objects.filter(user=self.request.user)
        return queryset
    

class CustomerOrderInvoiceView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    template_name = "dashboard/customer/orders/order-invoice.html"

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user,status=OrderStatusType.success.value)