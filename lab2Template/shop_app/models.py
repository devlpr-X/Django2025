from django.db import models
from django.db.models.fields import SlugField
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='images/categories', blank=True)
    
    def __str__ (self):
        return self.category_name
    
    class Meta:
        db_table = "tbl_categories" 

    def getUrl(self):
        return reverse('categoryDetail', kwargs={'slug': self.slug})

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='images/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def getUrl(self):
        return reverse("productDetail", kwargs= {
            "categorySlug": self.category.slug,
            "productSlug": self.slug
        })
        # return f"product/{self.category.slug}/{self.slug}"
    
    def __str__ (self):
        return self.product_name
    
    class Meta:
        db_table = "tbl_products"
