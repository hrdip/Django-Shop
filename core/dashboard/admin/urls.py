from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path('home/', views.AdminDashboardHomeView.as_view(), name="home"),
    path('security-edit/', views.AdminSecurityEditView.as_view(), name="admin-security-edit"),
    
]