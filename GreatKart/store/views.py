from ast import keyword
from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# from django.http import HttpResponse

# Create your views here.


def store(request, category_slug=None):
    """Function to load available products in store"""
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        # Refer to the Django docs and search Pagination
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products": paged_products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    """Function returns product details of products. If
    product is not in database, 404 page is dispalyed"""
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()  # Check if item is already available in the cart
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
    }

    return render(request, "store/product_detail.html", context)


def search(request):
    """Function to checks the keyword value from the search url"""
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            # Filter product descriptions or product names containing the keyword
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()

    context = {
        "products": products,
        "product_count": product_count,
        "keyword": keyword,
    }
    return render(request, "store/store.html", context)
