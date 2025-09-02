from django.db import models

class ProductCategory(models.Model):
    cname = models.CharField(max_length=100)

    def __str__(self):
        return self.cname


class Product(models.Model):
    pname = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.pname
