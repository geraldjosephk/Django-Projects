from ast import arg
from audioop import reverse
from unicodedata import category
from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    """Product model"""
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/Products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # Deletes entire product category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        """Function to link products in store to single product view page"""
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
