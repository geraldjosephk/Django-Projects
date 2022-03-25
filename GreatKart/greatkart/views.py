from difflib import context_diff
from django.shortcuts import render
from store.models import Product

# Pages for rendering


def home(request):
    # Display only products in  stock
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products,
    }
    return render(request, "home.html", context)
