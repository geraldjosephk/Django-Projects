from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.


class Cart(models.Model):
    """Class model for generating a cart"""

    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    """Class model for storing product in a cart"""

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Many to Many database relationship between variations,product and cart
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    # def __str__(self):
    #     return self.product

    def __unicode__(self):  # for displaying cart items properly in Django Admin
        return self.product
