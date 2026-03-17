from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    featured_products = Product.objects.all()[:8]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'categories': categories
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
