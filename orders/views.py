from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.views import get_cart
from .models import Order, OrderItem
from payments.models import Payment
from django.contrib import messages

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your bag is empty!")
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        # Simple checkout logic
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_price=cart.total_price
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.current_price,
                quantity=item.quantity
            )
        
        # Simulate payment selection
        payment_method = request.POST.get('payment_method')
        Payment.objects.create(
            order=order,
            method=payment_method,
            amount=order.total_price,
            transaction_id='GLOW-' + str(order.id) + 'XYZ',
            status='Success'
        )
        
        order.is_paid = True
        order.save()
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, "Order placed successfully!")
        return redirect('orders:order_success', order_id=order.id)
        
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})
