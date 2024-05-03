from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path('home/', views.CustomerDashboardHomeView.as_view(), name="home"),
    path('customer-security-edit/', views.CustomerSecurityEditView.as_view(), name="customer-security-edit"),
    path('customer-profile-edit/', views.CustomerProfileEditView.as_view(), name="customer-profile-edit"),
]
