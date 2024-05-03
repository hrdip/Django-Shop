from django.urls import path
from .. import views

urlpatterns = [
    path('security/edit/', views.AdminSecurityEditView.as_view(), name="admin-security-edit"),
    path('profile/edit/', views.AdminProfileEditView.as_view(), name="admin-profile-edit"),
    path('profile/image/edit/', views.AdminProfileImageEditView.as_view(), name="admin-profile-image-edit"),
]