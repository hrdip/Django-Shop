from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from order.permissions import HasCustomerAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import UserAddressModel

# Create your views here.
class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = UserAddressModel.objects.filter(user=self.request.user)
        return context