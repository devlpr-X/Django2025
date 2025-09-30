from django.contrib import admin
from django.urls import path
from shop_app import views
from django.conf.urls.static import static
from .settings import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("register/", views.register, name="register"),
    
    path("cart/", views.cart, name="cart"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/", views.search_result, name="search_result"),
    path("order_complete/", views.order_complete, name="order_complete"),
    path("place_order/", views.place_order, name="place_order"),

    path("<str:category_slug>/<str:product_slug>/", views.product_detail, name="product_detail_slug"),
    path("product_detail/", views.product_detail1, name="product_detail"),

    path('store/', views.store, name='store'),  
    path('<str:slug>/', views.store, name='store_by_category'),  

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
