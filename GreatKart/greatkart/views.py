from django.shortcuts import render
from store.models import Product, ReviewRating

# Pages for rendering


def home(request):
    # Display only products in  stock
    products = Product.objects.all().filter(is_available=True).order_by("created_date")

    # Get reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        "products": products,
        "reviews": reviews,
    }

    return render(request, "home.html", context)
