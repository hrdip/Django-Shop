from django.views.generic import View, TemplateView, FormView
from order.permissions import HasCustomerAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import UserAddressModel, OrderModel, OrderItemModel, CouponModel, OrderStatusType
from order.forms import CheckOutForm
from cart.models import CartModel
from django.urls import reverse_lazy
from website.models import NewsLetterModel
from website.forms import NewsLetterForm
from django.contrib import messages
from django.shortcuts import redirect
from cart.cart import CartSession
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from payment.zarinpal_client import ZarinPalSandbox
from payment.models import PaymentModel, PaymentStatusType
from django.db import transaction
from cart.models import CartItemModel
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
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        coupon = cleaned_data['coupon']

        cart = CartModel.objects.get(user=user)
        # make order with cart items we get
        order = self.create_order(address)

        # make order item with cart items we get
        self.create_order_items(order, cart)
        # after get cart_items for the order we need clean cart_items for next time order
        # remove product from cart
        self.clear_cart(cart)

        # get total price from cart_items and put on order total price form
        total_price = order.calculate_total_tax_price()

        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        payment_url = self.create_payment_url(order)

        # Check product availability before payment
        for item in order.order_items.all():
            if item.product.stock < item.quantity:
                messages.error(self.request, f"Sorry, {item.product.title} is out of stock.")
                return self.form_invalid(form)
        
        return redirect(payment_url)
    
    def create_payment_url(self, order):

        # after all before show complete order we need request to payment with our value and response from payment hub and connect user to payment hub
        zarinpal = ZarinPalSandbox()

        # amount come from order price afte tax and coupon cost
        response = zarinpal.payment_request(order.total_price)
        # create order payment object to fill up forms and we can see in admin django or admin user
        payment_obj = PaymentModel.objects.create(
            authority_id = response.get("Authority"),
            amount = order.total_price,
        )
        # replace payment object created to payment field into order models
        order.payment = payment_obj
        order.save()
        return (zarinpal.generate_payment_url(response.get("Authority")))
    
    # make order with cart items we get
    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )
    
    # make order item with cart items we et
    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                # order come from order object we make with OrderModel class in the create_order function
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

    # after get cart_items for the order we need clear cart_items for next time order
    # remove product from cart
    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            total_price = total_price - round((total_price * Decimal(coupon.discount_percent/100)))
            order.coupon = coupon
            # signal for detect this user used coupon
            coupon.used_by.add(user)
            coupon.save()

        order.total_price = total_price
        
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        cart = CartModel.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        total_price = cart.calculate_total_price()
        total_tax = round((total_price*9)/100)
        total_tax_price = total_price + total_tax
        total_discount = total_tax_price + 0
        context['addresses'] = UserAddressModel.objects.filter(user=self.request.user)
        context['total_price'] = total_price
        context['total_tax'] = total_tax
        context['total_tax_price'] = total_tax_price
        context['total_discount'] = total_discount
        return context
    

class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-completed.html'


class ValidateCouponView(LoginRequiredMixin, HasCustomerAccessPermission, View):
    
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        user = self.request.user
        status_code = 200
        message = "coupon successfully applied"
        total_price = 0
        total_tax = 0
        total_tax_price = 0
        total_discount = 0
        try:
            coupon = CouponModel.objects.get(code=code)
        
        except CouponModel.DoesNotExist:
            return JsonResponse({"message":"Invalid Coupon Code"}, status=404)
        
        # if coupon exists check expiration date, quantity of used coupon, used befor with same user
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code,message = 403,"Coupon limit exceeded"
            
            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code,message = 403,"Coupon Expired"
                
            
            elif user in coupon.used_by.all():
                status_code,message = 403,"Coupon already used"

            else:
                cart = CartModel.objects.get(user=self.request.user)
                total_price = cart.calculate_total_price()
                total_tax = round((total_price*9)/100)
                total_tax_price = total_price + total_tax
                total_discount = round(total_tax_price - (total_tax_price * (coupon.discount_percent/100)))
        return JsonResponse({"message":message, "total_tax":total_tax, "total_tax_price":total_tax_price, "total_discount":total_discount, "total_price":total_price}, status=status_code)


class OrderFailedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-failed.html'


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