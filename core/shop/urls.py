from django.urls import path, re_path
from . import views

app_name = "shop"

urlpatterns = [
    path("product/grid/", views.ShopProductGridView.as_view(),name="product-grid"),
    path("product/list/", views.ShopProductListView.as_view(),name="product-list"),
    # path("product/<slug:slug>/detail/", views.ShopProductDetailView.as_view(),name="product-detail"),
    # support persian slug
    re_path(r"product/(?P<slug>[-\w]+)/detail/", views.ShopProductDetailView.as_view(),name="product-detail"),
    path("news-letter-view/", views.NewsLetterView.as_view(),name="news-letter"),
    path("add-or-remove-wishlist/", views.AddOrRemoveWishlistView.as_view(),name="add-or-remove-wishlist"),
]
