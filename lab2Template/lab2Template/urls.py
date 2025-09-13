from django.contrib import admin
from django.urls import path
from shop_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("cart/", views.cart, name="cart"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("order_complete/", views.order_complete, name="order_complete"),
    # path("product/", views.product_detail, name="product_detail"),
    path("product_detail/", views.product_detail, name="product_detail"),
    path("register/", views.register, name="register"),
    path("search/", views.search_result, name="search_result"),
    path("signin/", views.signin, name="signin"),
    path("store/", views.store, name="store"),
    path("place_order/", views.place_order, name="place_order"),
]
