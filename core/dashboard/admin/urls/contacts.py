from django.urls import path,include
from .. import views


urlpatterns = [
    path("contact/list/", views.AdminContactListView.as_view(), name="admin-contact-list"),
    path("contact/<int:pk>/detail/", views.AdminContactDetailView.as_view(), name="admin-contact-detail"),
]