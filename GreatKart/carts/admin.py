from django.contrib import admin
from .models import Cart, CartItem

# Register your models here for use in Django Admin interface


class CartAdmin(admin.ModelAdmin):
    """Class admin model for displaying cart_id, and date product was added"""
    list_display = ('cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    """Class admin model for displaying product,cart,quantity,activity"""
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
