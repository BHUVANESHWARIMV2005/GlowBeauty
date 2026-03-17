from .models import Cart

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = sum(item.quantity for item in cart.items.all())
    else:
        # For anonymous users, we could use session-based cart
        pass
    return {'cart_count': count}
