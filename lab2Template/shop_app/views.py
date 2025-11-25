from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from cart_app.models import Cart, CartItem
from cart_app.views import _cart_id
from django.core.paginator import Paginator
from django.db import connection
from .models import Category, Product
import sqlite3

def index(request):
    products = Product.objects.order_by('-created_date')[:4]
    print(products)
    return render(request, 'index.html', {'products': products, 'count': products.count()})


def cart(request):
    return render(request, "cart.html")


def dashboard(request):
    return render(request, "dashboard.html")

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category, Product, ImageGallery
from cart_app.models import CartItem
from cart_app.views import _cart_id

def product_detail(request, categorySlug, productSlug):
    category = get_object_or_404(Category, slug=categorySlug)
    product = get_object_or_404(Product, slug=productSlug, category=category)

    in_cart = CartItem.objects.filter(cart__id=_cart_id(request), product=product).exists()

    # энд ImageGallery-аас тухайн бүтээгдэхүүний бүх зураг авна
    product_images = ImageGallery.objects.filter(product=product)

    context = {
        'single_product': product,
        'in_cart': in_cart,
        'product': product,
        'category': category,
        'product_images': product_images,  # Шинэ нэмэлт
    }
    return render(request, 'product-detail.html', context)



def register(request):
    return render(request, "register.html")


def search_result(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(
                Q(product_name__icontains=keyword)|
                Q(description__icontains=keyword)
            )

            count = products.count()
    context = {  
        "products": products,
        "count": count,
        "keyword": keyword,
    }
    return render(request, "store.html",context) 


def signin(request):
    return render(request, "signin.html")

def store(request, slug=None):
    categories = Category.objects.all()
    products_list = Product.objects.filter(is_available=True)

    keyword = request.GET.get('keyword', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    selected_category = None
    selected_category_obj = None

    # 1. slug-аар фильтр
    if slug:
        selected_category_obj = get_object_or_404(Category, slug=slug)
        selected_category = slug
        products_list = products_list.filter(category=selected_category_obj)

    # 2. Query параметрээр категори
    category_param = request.GET.get('category', '')
    if category_param and not slug:
        try:
            selected_category_obj = Category.objects.get(slug=category_param)
            selected_category = category_param
            products_list = products_list.filter(category=selected_category_obj)
        except Category.DoesNotExist:
            pass

    # 3. Хайлтын түлхүүр үг
    if keyword:
        products_list = products_list.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        ).distinct()

    # 4. Үнийн доод хязгаар
    if min_price:
        try:
            min_price_int = int(min_price)
            products_list = products_list.filter(price__gte=min_price_int)
        except ValueError:
            min_price = ''

    # 5. Үнийн дээд хязгаар
    if max_price:
        try:
            max_price_int = int(max_price)
            products_list = products_list.filter(price__lte=max_price_int)
        except ValueError:
            max_price = ''

    # Сорт
    products_list = products_list.order_by('-created_date')

    # Хуудаслалт
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': products,
        'count': products_list.count(),
        'selected_category': selected_category,
        'selected_category_obj': selected_category_obj,
        'keyword': keyword,
        'min_price': min_price,
        'max_price': max_price,
    }
    print(context)
    return render(request, 'store.html', context)


# def store(request, slug=None):
#     categories = Category.objects.all()
#     products_list = Product.objects.all()

#     if slug:
#         category = get_object_or_404(Category, slug=slug)
#         products_list = products_list.filter(category=category)

#     paginator = Paginator(products_list, 5)
#     page_number = request.GET.get('page')
#     products = paginator.get_page(page_number)

#     context = {
#         'categories': categories,
#         'products': products,
#         'count': products_list.count()
#     }
#     return render(request, 'store.html', context)


def search(request):
    """
    Хайлтын функц - түлхүүр үг + үнэ + категори
    """
    keyword = request.GET.get('keyword', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    category_slug = request.GET.get('category', '')

    # Эхлээд бүх идэвхтэй бүтээгдэхүүн авах
    products = Product.objects.filter(is_available=True)

    # 1. Категориор шүүлтүүлэх
    selected_category_obj = None
    if category_slug:
        try:
            selected_category_obj = Category.objects.get(slug=category_slug)
            products = products.filter(category=selected_category_obj)
        except Category.DoesNotExist:
            pass

    # 2. Түлхүүр үг хайх
    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        ).distinct()

    # 3. Үнийн доод хязгаар
    if min_price:
        try:
            min_price_int = int(min_price)
            products = products.filter(price__gte=min_price_int)
        except ValueError:
            min_price = ''

    # 4. Үнийн дээд хязгаар
    if max_price:
        try:
            max_price_int = int(max_price)
            products = products.filter(price__lte=max_price_int)
        except ValueError:
            max_price = ''

    # Сортлох (шинэ эхлүүлээр)
    products = products.order_by('-created_date')

    count = products.count()

    # Хуудаслалт
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    

    context = {
        'products': paged_products,
        'count': count,
        'keyword': keyword,
        'min_price': min_price,
        'max_price': max_price,
        'selected_category': category_slug,
        'selected_category_obj': selected_category_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'store.html', context)

def search2(request):
    keyword = request.GET.get('keyword', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    # Түлхүүр үг хайх
    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        ).distinct()

    # Үнийн доод хязгаар
    if min_price:
        try:
            min_price = int(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass

    # Үнийн дээд хязгаар
    if max_price:
        try:
            max_price = int(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass

    count = products.count()

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'count': count,
        'keyword': keyword,
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
    }
    return render(request, 'store.html', context)

def search1(request, category_slug=None):
    categories = Category.objects.raw("SELECT * FROM tbl_categories")

    keyword = request.GET.get('keyword', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_category = request.GET.get('category')

    query = "SELECT * FROM tbl_products WHERE is_available = 1"
    params = []

    if keyword:
        query += " AND product_name LIKE %s"
        params.append(f"%{keyword}%")
    if min_price:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)
    if selected_category:
        query += " AND category_id = (SELECT id FROM tbl_categories WHERE slug = %s)"
        params.append(selected_category)
    if category_slug:
        query += " AND category_id = (SELECT id FROM tbl_categories WHERE slug = %s)"
        params.append(category_slug)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in rows]

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = len(products)

    context = {
        'categories': categories,
        'products': paged_products,
        'count': count,
        'keyword': keyword,
        'min_price': min_price,
        'max_price': max_price,
        'selected_category': selected_category,
    }
    return render(request, 'search-result.html', context)

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



# def search(request, category_slug=None):
#     keyword = request.GET.get('keyword', '')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')
#     selected_category = request.GET.get('category')

#     base_query = "SELECT * FROM tbl_products WHERE is_available = TRUE"
#     params = []

#     if keyword:
#         base_query += " AND product_name LIKE %s"
#         params.append(f"%{keyword}%")

#     if min_price:
#         base_query += " AND price >= %s"
#         params.append(min_price)

#     if max_price:
#         base_query += " AND price <= %s"
#         params.append(max_price)

#     if selected_category:
#         base_query += """ AND category_id IN (
#             SELECT id FROM store_category WHERE slug = %s
#         )"""
#         params.append(selected_category)

#     if category_slug:
#         base_query += """ AND category_id IN (
#             SELECT id FROM store_category WHERE slug = %s
#         )"""
#         params.append(category_slug)

#     base_query += " ORDER BY id ASC"

#     products = Product.objects.raw(base_query, params)
#     products_list = list(products)

#     paginator = Paginator(products_list, 6)
#     page = request.GET.get('page')
#     paged_products = paginator.get_page(page)
#     product_count = len(products_list)

#     categories = Category.objects.all()

#     context = {
#         'categories': categories,
#         'products': paged_products,
#         'count': product_count,
#         'keyword': keyword,
#         'min_price': min_price,
#         'max_price': max_price,
#         'selected_category': selected_category,
#     }
#     return render(request, 'store.html', context)
# import sqlite3 as sql

# con = sql.connect("db.sqlite3")
# con.row_factory = sql.Row
# cur = con.cursor()

# # бүх бүтээгдэхүүн
# cur.execute("SELECT * FROM tbl_product")
# all_products = cur.fetchall()

# # id=1 бүтээгдэхүүн
# cur.execute("SELECT * FROM tbl_product WHERE id=1")
# product_by_id = cur.fetchall()

# # нэрээр хайлт
# cur.execute("""SELECT * FROM tbl_product 
#                 WHERE LOWER(product_name)='%pro%'
#                 OR LOWER(description)='%pro%'""")
# product_by_name = cur.fetchall()

# con.close()
