from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    #path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # for register user
    path('register/', views.RegisterUserView.as_view(), name='register'),
  
]
