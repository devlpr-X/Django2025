from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models import Avg

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
    images = models.ImageField(upload_to='images/products', blank=True, null=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def average_rating(self):
        """Бүтээгдэхүүний сэтгэгдлүүдээс дундаж үнэлгээ буцаана"""
        result = self.reviews.aggregate(avg=Avg("rating"))
        return round(result["avg"] or 0, 2)

    def rating_percent(self):
        """Front-end progress bar-д ашиглах хувь (%)"""
        avg = self.average_rating()
        return (avg / 5) * 100 if avg > 0 else 0

    def getUrl(self):
        return reverse("product_detail", kwargs={
            "categorySlug": self.category.slug,
            "productSlug": self.slug
        })

    class Meta:
        db_table = "tbl_products"

    def __str__(self):
        return self.product_name


class ImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='images/products/gallery', max_length=255)

    class Meta:
        db_table = "tbl_product_images"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.product_name} - {self.id}"


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()  # 1.0 - 5.0
    created_date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "store_reviewrating"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.rating})"