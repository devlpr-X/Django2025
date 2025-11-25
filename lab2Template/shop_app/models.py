from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='images/categories', blank=True)

    def __str__(self):
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
    images = models.ImageField(upload_to='images/products', blank=True, null=True)  # primary image
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def getUrl(self):
        return reverse("product_detail", kwargs={
            "categorySlug": self.category.slug,
            "productSlug": self.slug
        })

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "tbl_products"


class ImageGallery(models.Model):
    """
    Нэг бүтээгдэхүүнд олон зураг хамаарах загвар
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='images/products/gallery', max_length=255)

    def __str__(self):
        return f"{self.product.product_name} - {self.id}"

    class Meta:
        db_table = "tbl_product_images"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
