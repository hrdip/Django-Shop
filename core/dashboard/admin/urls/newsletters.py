from django.urls import path
from .. import views

urlpatterns = [
    path("newsletter/list/", views.AdminNewsletterListView.as_view(), name="newsletter-list"),
    path("newsletter/<int:pk>/delete/", views.AdminNewsletterDeleteView.as_view(), name="newsletter-delete"),
]
