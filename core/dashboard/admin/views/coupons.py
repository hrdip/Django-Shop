from django.views.generic import (
    UpdateView,
    ListView,
    DeleteView,
    CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import AdminCouponForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.core.exceptions import FieldError
from order.models import CouponModel
# Create your views here.

class AdminCouponListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = 'dashboard/admin/coupons/coupon-list.html'
    paginate_by = 10 

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    # filters and get response
    def get_queryset(self):
        queryset = CouponModel.objects.all()
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(code__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context
    

class AdminCouponCreateView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'dashboard/admin/coupons/coupon-create.html'
    form_class = AdminCouponForm
    queryset = CouponModel.objects.all()
    success_message = "Coupon was successfully created"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk":form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-list")
    

class AdminCouponEditView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/admin/coupons/coupon-edit.html'
    form_class = AdminCouponForm
    queryset = CouponModel.objects.all()
    success_message = "Coupon was successfully updated"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk":self.get_object().pk})

    

class AdminCouponDeleteView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/admin/coupons/coupon-delete.html'
    queryset = CouponModel.objects.all()
    success_message = "Coupon was successfully deleted"
    success_url = reverse_lazy("dashboard:admin:coupon-list")
