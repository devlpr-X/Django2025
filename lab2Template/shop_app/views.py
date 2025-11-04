from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
from cart_app.models import CartItem
from cart_app.views import _cart_id

def index(request):
    products = Product.objects.order_by('-created_date')[:4]
    return render(request, 'index.html', {'products': products, 'count': products.count()})

def cart(request):
    return render(request, "cart.html")

def dashboard(request):
    return render(request, "dashboard.html")

def order_complete(request):
    return render(request, "order_complete.html")

def product_detail(request, categorySlug, productSlug):
    category = get_object_or_404(Category, slug=categorySlug)
    product = get_object_or_404(Product, slug=productSlug, category=category)
    in_cart = CartItem.objects.filter(cart__id=_cart_id(request), product=product).exists()
    return render(request, 'product-detail.html', {
        'single_product': product, 
        'in_cart': in_cart, 
        'product': product, 
        'category': category
    })

def register(request):
    return render(request, "register.html")

def search_result(request):
    return render(request, "search-result.html")

def signin(request):
    return render(request, "signin.html")

def store(request, slug=None):
    categories = Category.objects.all()
    products_list = Product.objects.all()

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products_list = products_list.filter(category=category)

    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': products,
        'count': products_list.count()
    }
    return render(request, 'store.html', context)

def place_order(request):
    return render(request, "place_order.html")
