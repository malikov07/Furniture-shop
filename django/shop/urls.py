from django.urls import path
from .views import (
    AddToCartView,
    ShopView,
    ProductDetailView,
    CartView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("add-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("", ShopView.as_view(), name="shop"),
    path("create/", ProductCreateView.as_view(), name="shop-create"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
    path("update/<int:id>/", ProductUpdateView.as_view(), name="shop-update"),
    path("delete/<int:id>/", ProductDeleteView.as_view(), name="shop-delete"),
]

