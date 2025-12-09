from django.contrib import admin
from django.urls import path, include
from shop_app import views
from django.conf.urls.static import static
from .settings import *

# Model get_url() function###################

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",            views.index,    name="index"),
    path("signin/",     views.signin,   name="signin"),
    path("register/",   views.register, name="register"),
    
    path("accounts/",       include('accounts.urls'),          name="accounts"),
    path("cart/",           include('cart_app.urls'),          name="cart"),
    path("store/",          include('shop_app.urls'),          name="store"),
    path("cart/",           views.cart,          name="cart"),
    path("dashboard/",      views.dashboard,     name="dashboard"),
    path("search/",         views.search_result, name="search_result"),
    path("order_complete/", views.order_complete,name="order_complete"),
    path("place_order/",    views.place_order,   name="place_order"),

    path("submit_review/<int:product_id>/", views.submit_review, name="submit_review"),
    path("<slug:categorySlug>/<slug:productSlug>/", views.product_detail, name="product_detail"),
    path("<str:slug>/", views.store, name="categoryDetail"),

    # path("<slug:categorySlug>/<slug:productSlug>",     views.product_detail,  name="product_detail"),
    # path('<slug:categorySlug>/<slug:productSlug>/', views.product_detail, name='product_detail'),
    # path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    # path('<str:slug>/', views.store, name='categoryDetail'),  

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
