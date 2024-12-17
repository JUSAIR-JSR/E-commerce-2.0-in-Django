from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from cart.models import CartItem

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required(login_url='login')
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)

    orders = []
    total_price = 0

    for item in cart_items:
        total_price += item.quantity * item.product.price
        orders.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item.quantity * item.product.price
        })

    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.quantity * item.product.price
            )
        cart_items.delete()
        return redirect('order_history')

    return render(request, 'orders/checkout.html', {'orders': orders, 'total_price': total_price})
