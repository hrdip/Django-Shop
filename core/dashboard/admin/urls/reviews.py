from django.urls import path
from .. import views

urlpatterns = [
    path('review/list/', views.AdminReviewListView.as_view(), name="admin-review-list"),
    path('review/<int:pk>/edit/', views.AdminReviewEditView.as_view(), name="admin-review-edit"),
]