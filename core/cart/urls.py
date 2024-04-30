from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("session/add-product/", views.SessionAddProductView.as_view(), name="session-add-product"),
    path("session/cart/summery/", views.SessionCartSummeryView.as_view(), name="session-cart-summery"),
    path("session/update-product-quantity/", views.SessionUpdateProductQuantityView.as_view(), name="session-update-product-quantity"),
    path("session/remove-product/", views.SessionRemoveProductView.as_view(), name="session-remove-product"),
]
