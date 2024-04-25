from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("session/add-product/", views.SessionAddProduct.as_view(), name="session-add-product"),
    path("session/cart/summery/", views.SessionCartSummery.as_view(), name="session-cart-summery"),
]
