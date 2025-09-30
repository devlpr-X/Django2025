import sqlite3 as sql
from shop_app.models import Category


def categoriesProcessor(request):
    categories = Category.objects.all() 
    return {'categories': categories}    
