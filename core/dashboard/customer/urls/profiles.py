from django.urls import path
from .. import views

urlpatterns = [
    path('security/edit/', views.CustomerSecurityEditView.as_view(), name="customer-security-edit"),
    path('profile/edit/', views.CustomerProfileEditView.as_view(), name="customer-profile-edit"),
    path('profile/image/edit/', views.CustomerProfileImageEditView.as_view(), name="customer-profile-image-edit"),
]
