from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/", views.OrderCheckoutView.as_view(),name="checkout"),
    path("completed/", views.OrderCompletedView.as_view(),name="order-completed"),
    path("validate-coupon/", views.ValidateCouponView.as_view(),name="validate-coupon"),
    path("failed/", views.OrderFailedView.as_view(),name="order-failed"),

]
