from django import forms
from .models import Product, ProductCategory

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['cname']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pname','category', 'price']
