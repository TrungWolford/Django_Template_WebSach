from django.db import models

# Create your models here.
class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    status = models.IntegerField(default=1)  # 0: Huy, 1: Dang hoat dong

    def __str__(self):
        return self.categoryName

class Product(models.Model):
    productName = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category, related_name="products")  # ManyToMany
    image = models.JSONField(blank=True, null=True)  # list of strings
    author = models.CharField(max_length=100, blank=True)
    cover = models.CharField(max_length=200, blank=True)
    price = models.BigIntegerField(default=0)
    stock = models.BigIntegerField(default=0)
    description = models.TextField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)  # 0: Ngung hoat dong, 1: Dang hoat dong

    def __str__(self):
        return self.productName
