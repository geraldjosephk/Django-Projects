from tabnanny import verbose
from django.db import models
from distutils.command.upload import upload


class Category(models.Model):
    """ Specifying name,slug,description,visual image of category"""
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    # Define plural in django admin
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
