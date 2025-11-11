from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from cart_app.models import Cart, CartItem
from cart_app.views import _cart_id


def index(request):
    products = Product.objects.order_by('-created_date')[:4]
    return render(request, 'index.html', {'products': products, 'count': products.count()})


def cart(request):
    return render(request, "cart.html")


def dashboard(request):
    return render(request, "dashboard.html")


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


def search(request):
    keyword = request.GET.get('keyword')

    products = Product.objects.all()
    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        ).distinct()
    else:
        products = Product.objects.none()

    count = products.count()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'count': count,
    }
    return render(request, 'store.html', context)


def place_order(request):
    cart_id = _cart_id(request)
    cart_items = CartItem.objects.filter(cart__id=cart_id, is_active=True)

    total = sum(item.sub_total() for item in cart_items)
    tax = total * 0.02  # 2% татвар
    grand_total = total + tax

    if request.method == "POST":
        order_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'address_country': request.POST.get('address_country'),
            'address_region': request.POST.get('address_region'),
            'address_street': request.POST.get('address_street'),
            'address_building': request.POST.get('address_building'),
            'address_apartment': request.POST.get('address_apartment'),
            'postal_code': request.POST.get('postal_code'),
            'zip_code': request.POST.get('zip_code'),
            'total': grand_total,
            'tax': tax,
        }
        request.session['order_data'] = order_data

        messages.success(request, "Таны захиалгын мэдээлэл хадгалагдлаа.")
        return redirect('order_complete')

    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand': grand_total,
    }
    return render(request, 'place_order.html', context)


def order_complete(request):
    cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        cart = None

    cart_items = CartItem.objects.filter(cart=cart, is_active=True) if cart else []
    order_data = request.session.get('order_data', None)

    context = {
        'cart_items': cart_items,
        'order_data': order_data,
    }
    return render(request, 'order_complete.html', context)
