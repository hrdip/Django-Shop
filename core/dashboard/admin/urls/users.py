from django.urls import path,include
from .. import views


urlpatterns = [
    path("user/list/", views.AdminUserListView.as_view(), name="admin-user-list"),
    path("user/<int:pk>/delete/", views.AdminUserDeleteView.as_view(), name="admin-user-delete"),
    path("user/<int:pk>/edit/", views.AdminUserUpdateView.as_view(), name="admin-user-edit"),
]