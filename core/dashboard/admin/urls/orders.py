from django.urls import path
from .. import views

urlpatterns = [
    path("order/list/", views.AdminOrderListView.as_view(), name="admin-order-list"),
    path("order/<int:pk>/detail/", views.AdminOrderDetailView.as_view(), name="admin-order-detail"),
    path("order/<int:pk>/invoice/",views.AdminOrderInvoiceView.as_view(),name="admin-order-invoice"),
]
