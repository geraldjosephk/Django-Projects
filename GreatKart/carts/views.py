from itertools import product
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem

from django.http import HttpResponse

# Create your views here.


def _cart_id(request):
    """Function to capture or create session id  of the cart"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """Function add item to cart and to increase item number"""
    product = Product.objects.get(id=product_id)  # get product
    try:
        # get cart using the cart id in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # increase cart item by 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')


def remove_cart(request, product_id):
    """Function to decrease item number in the cart"""
    cart = Cart.objects.get(cart_id=_cart_id(
        request))  # get get cart session id
    # show item in cart or show not available page
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart)  # fetch items in cart
    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # decrease cart item by 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    """Function to remove item from cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    """Function to display what is avaible in the cart"""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(
            request))  # get cart session id
        # filter products in present the cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            # get total price of all items in cart
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity  # Get current number of items
        tax = (2*total)/100
        grand_total = total + tax
    except ObjectNotExist:
        pass  # If no items available in the cart,ignore

    context = {
        'total': total,
        'quuantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
