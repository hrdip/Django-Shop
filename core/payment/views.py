from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType
from django.db import transaction
# Create your views here.

class PaymentVerifyView(View):

    # after redirect from payment hub we need to get parameters
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get('Authority')
        status = request.GET.get('Status')

        # check this payment for us
        payment_obj = get_object_or_404(PaymentModel,authority_id=authority_id)

        # request to zarinpal
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_verify(int(payment_obj.amount),payment_obj.authority_id)

        order = OrderModel.objects.get(payment=payment_obj)

        if response["Status"] == 100 or response["Status"] == 101:
            payment_obj.ref_id = response["RefID"]
            payment_obj.response_code = response["Status"]
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.response_json = response
            payment_obj.save()

            # change order status same as payment status
            order.status = OrderStatusType.success.value
            order.save()

            # Decrease the stock quantity of products in the order
            with transaction.atomic():
                for item in order.order_items.all():
                    product = item.product
                    product.stock -= item.quantity
                    product.save()

            return redirect(reverse_lazy("order:order-completed"))
        else: 
            payment_obj.ref_id = response["RefID"]
            payment_obj.response_code = response["Status"]
            payment_obj.status = PaymentStatusType.faild.value
            payment_obj.response_json = response
            payment_obj.save()

            # change order status same as payment status
            order.status = OrderStatusType.failed.value
            order.save()
            return redirect(reverse_lazy("order:order-failed"))