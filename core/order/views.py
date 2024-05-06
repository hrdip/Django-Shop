from django.shortcuts import render
from django.views.generic import TemplateView
from order.permissions import HasCustomerAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/checkout.html'