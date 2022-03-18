from django.contrib import admin
from .models import Product, Variation
# Register your models here.


class Productadmin(admin.ModelAdmin):
    """Class admin model for displaying product_name,price,stock amount, category
    modified date and availability """
    list_display = ('product_name', 'price', 'stock',
                    'category', 'modified_date', 'is_available')
    # field that fill themselves
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    """Class admin model for displaying product,variation category,value,activity and date.
    is__active field is editable. One can filter variations by product,variation category
    ,value,activity and date."""
    list_display = ('product', 'variation_category', 'variation_value',
                    'is_active', 'created_date')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category',
                   'variation_value', 'created_date')


# Register models
admin.site.register(Product, Productadmin)
admin.site.register(Variation, VariationAdmin)
