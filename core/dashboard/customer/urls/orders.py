from django.urls import path
from .. import views

urlpatterns = [
    path("order/list/", views.CustomerOrderListView.as_view(), name="customer-order-list"),
    path("order/<int:pk>/detail/", views.CustomerOrderDetailView.as_view(), name='customer-order-detail'),

]
