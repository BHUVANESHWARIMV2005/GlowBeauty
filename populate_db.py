import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glowbeauty.settings')
django.setup()

from products.models import Category, Product

def populate():
    categories = [
        ('Skincare', 'skincare'),
        ('Makeup', 'makeup'),
        ('Haircare', 'haircare'),
        ('Fragrance', 'fragrance'),
        ('Beauty Tools', 'beauty-tools'),
    ]

    for name, slug in categories:
        Category.objects.get_or_create(name=name, slug=slug)

    # Sample Products
    skincare = Category.objects.get(slug='skincare')
    makeup = Category.objects.get(slug='makeup')
    haircare = Category.objects.get(slug='haircare')

    products = [
        {
            'name': 'Radiance Glow Serum',
            'brand': 'Lumina',
            'category': skincare,
            'description': 'A lightweight serum that instantly brightens and hydrates the skin.',
            'price': 45.00,
            'stock': 100,
            'rating': 4.8
        },
        {
            'name': 'Velvet Matte Lipstick',
            'brand': 'Vivid',
            'category': makeup,
            'description': 'Long-lasting matte lipstick with a comfortable, velvety finish.',
            'price': 25.00,
            'discount_price': 18.00,
            'stock': 50,
            'rating': 4.5
        },
        {
            'name': 'Silk Touch Conditioner',
            'brand': 'Gloss',
            'category': haircare,
            'description': 'Deeply nourishing conditioner for silky, manageable hair.',
            'price': 30.00,
            'stock': 75,
            'rating': 4.7
        },
        {
            'name': 'Midnight Rose Perfume',
            'brand': 'Essence',
            'category': Category.objects.get(slug='fragrance'),
            'description': 'A mysterious and elegant floral scent with notes of rose and amber.',
            'price': 85.00,
            'stock': 30,
            'rating': 4.9
        }
    ]

    for p_data in products:
        Product.objects.get_or_create(**p_data)

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
