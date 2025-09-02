from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='productList'),
    path('category/<int:pk>/', views.ProductByCategoryView.as_view(), name='productsByCategory'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='productDetail'),    
    
    #crud
    path('product/add/', views.baraa, name='productAdd'),
    # path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='productEdit'),
    # path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='productDelete'),
]
