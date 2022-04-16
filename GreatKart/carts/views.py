from calendar import c
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    """Function to capture or create session id  of the cart"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """
    Function adds item to cart with variations.
    Accepts product_id as an argument.
    """

    # Getting product variation
    product = Product.objects.get(id=product_id)  # get product
    product_variation = []  # List to contain product variations
    if request.method == "POST":  # if a POST request
        for item in request.POST:
            key = item  # variation type
            value = request.POST[key]  # variation value

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )  # iexact means ignore the case of word
                # print(variation)
                product_variation.append(variation)
            except:
                pass
    # return HttpResponse(color + ' ' + size)
    # exit()

    # Getting cart
    try:
        # get cart using the cart id in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        # if cart does not exist, create new cart and save it
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # Getting cart items
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        # fetch existing variations in database
        # display current product variation
        # fetch item id in database
        existing_variations_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variations_list.append(list(existing_variation))
            id.append(item.id)
        print(existing_variations_list, id)

        if product_variation in existing_variations_list:
            # Increase the cart item quantity
            index = existing_variations_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            # create new cart item
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:  # Check if product_variation array is empty
                item.variations.clear()  # clear previous variations
                item.variations.add(
                    *product_variation
                )  # display all product variations
            item.save()

    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:  # Check if product_variation array is empty
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)

        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect("cart")


def remove_cart(request, product_id, cart_item_id):
    """
    Function to decrease item number in the cart.
    Accepts product_id, and cart_item_id as argumnts.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))  # get get cart session id
    # show item in cart or show not available page
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id
        )  # fetch items in cart
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # decrease cart item by 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect("cart")


def remove_cart_item(request, product_id, cart_item_id):
    """Function to remove item from cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart")


def cart(request, total=0, quantity=0, cart_items=None):
    """
    Function to display what is avaible in the cart.
    Accepts total,quantity and cart_items as arguments.
    """
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get cart session id
        # filter products in present the cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            # get total price of all items in cart
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity  # Get current number of items
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # If no items available in the cart,ignore

    context = {
        "total": total,
        "quuantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "store/cart.html", context)


@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get cart session id
        # filter products in present the cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            # get total price of all items in cart
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity  # Get current number of items
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # If no items available in the cart,ignore

    context = {
        "total": total,
        "quuantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "store/checkout.html", context)
