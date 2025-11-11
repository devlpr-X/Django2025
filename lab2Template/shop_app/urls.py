from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:slug>/', views.store, name='products_by_category'),
    path('search/', views.search, name='search'),
]
