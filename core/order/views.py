from django.views.generic import View, TemplateView, FormView
from order.permissions import HasCustomerAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import UserAddressModel, OrderModel, OrderItemModel
from order.forms import CheckOutForm
from cart.models import CartModel
from django.urls import reverse_lazy
from website.models import NewsLetterModel
from website.forms import NewsLetterForm
from django.contrib import messages
from django.shortcuts import redirect
from cart.cart import CartSession
# Create your views here.


class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = 'order/checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy("order:order-completed")

    def get_form_kwargs(self):
        kwargs = super(OrderCheckoutView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        cart = CartModel.objects.get(user=self.request.user)
        # get caet_items
        cart_items = cart.cart_items.all()
        # make order with cart items we et
        order = OrderModel.objects.create(
            user = self.request.user,
            address = address.address,
            state = address.state,
            city = address.city,
            zip_code = address.zip_code,
        )
        # make order item with cart items we et
        for item in cart_items:
            OrderItemModel.objects.create(
                # order come from order object we make with OrderModel class in the top line
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.get_price(),
            )
        # after get cart_items for the order we need clean cart_items for next time order
        # remove product from cart
        cart_items.delete()
        CartSession(self.request.session).clear()
        order.total_price = order.calculate_total_price()
        order.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

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
    
class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-completed.html'

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