from django.contrib import admin
from django.urls import path
from shop_app import views
from django.conf.urls.static import static
from .settings import *

# Model get_url() function###################

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",            views.index,    name="index"),
    path("signin/",     views.signin,   name="signin"),
    path("register/",   views.register, name="register"),
    
    path("cart/",           views.cart,          name="cart"),
    path("dashboard/",      views.dashboard,     name="dashboard"),
    path("search/",         views.search_result, name="search_result"),
    path("order_complete/", views.order_complete,name="order_complete"),
    path("place_order/",    views.place_order,   name="place_order"),

    path("<slug:categorySlug>/<slug:productSlug>",     views.productDetail,  name="productDetail"),

    path('store/',      views.store, name='store'),  
    path('<str:slug>/', views.store, name='categoryDetail'),  

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
