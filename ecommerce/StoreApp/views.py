from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from .models import Product, ProductCategory
from .forms import ProductForm

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'store/productList.html'
    context_object_name = 'products'

class ProductByCategoryView(ListView):
    model = Product
    template_name = 'store/productList.html'

    def getQuerySet(self):
        return Product.objects.filter(category_id = self.kwargs['pk'])

class ProductDetailView(DetailView):
    model = Product
    template_name = "store/productDetail.html"

def baraa(request):
    model = Product
    bform = ProductForm
    return render(request, 'productForm.html', {'bform' : bform})
# class ProductCreateView(CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'store/productForm.html'
#     success_url = reverse_lazy('productList')










# class ProductUpdateView(UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'store/productForm.html'
#     success_url = reverse_lazy('productList')

# class ProductDeleteView(DeleteView):
#     model = Product
#     template_name = 'store/productConfirmDelete.html'
#     success_url = reverse_lazy('productList')