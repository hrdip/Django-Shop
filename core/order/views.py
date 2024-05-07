from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from order.permissions import HasCustomerAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import UserAddressModel
from order.forms import CheckOutForm
from cart.models import CartModel

# Create your views here.
class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = 'order/checkout.html'
    form_class = CheckOutForm

    def get_context_data(self, **kwargs):
        cart = CartModel.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        total_price = cart.calculate_total_price()
        total_tax = round((total_price*9)/100)
        total_tax_price = total_price + total_tax
        context['addresses'] = UserAddressModel.objects.filter(user=self.request.user)
        context['total_price'] = total_price
        context['total_tax'] = total_tax
        context['total_tax_price'] = total_tax_price

        return context