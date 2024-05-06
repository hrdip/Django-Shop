from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.IndexView.as_view(),name="index"),
    path("contact/", views.ContactUsView.as_view(),name="contact"),
    path("about/", views.AboutView.as_view(),name="about"),
    path("news-letter-view/", views.NewsLetterView.as_view(),name="news-letter"),
]
