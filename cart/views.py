from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required(login_url='login')
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('view_cart')
