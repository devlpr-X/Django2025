import os
import sys
import django
from django.db import connection

# parent хавтас руу path нэмэх
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab2Template.settings")
django.setup()

def runme():
    with connection.cursor() as cursor:
        cursor.execute("""
            ALTER TABLE shop_app_category RENAME TO tbl_categories;
            ALTER TABLE shop_app_product RENAME TO tbl_products;
        """)
        cursor.execute()
        # tables = [row[0] for row in cursor.fetchall()]
        # print(tables)

if __name__ == "__main__":
    runme()
