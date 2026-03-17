import os
import urllib.request
import django
import ssl  # Added for SSL bypass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glowbeauty.settings')
django.setup()

from django.conf import settings
from products.models import Category, Product

def download_image(url, path):
    try:
        print(f"Downloading {url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Create context to ignore SSL verification (common issue on macOS)
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=context) as response, open(path, 'wb') as out_file:
            out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def setup_images():
    base_media = settings.MEDIA_ROOT
    print(f"Using media directory: {base_media}")
    os.makedirs(os.path.join(base_media, 'categories'), exist_ok=True)
    os.makedirs(os.path.join(base_media, 'products'), exist_ok=True)

    # Image URLs from Unsplash (High quality cosmetics)
    data = {
        'categories': {
            'skincare': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&q=80&w=400',
            'makeup': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&q=80&w=400',
            'haircare': 'https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&q=80&w=400',
            'fragrance': 'https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&q=80&w=400',
            'beauty-tools': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?auto=format&fit=crop&q=80&w=400'
        },
        'products': {
            'Radiance Glow Serum': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=600',
            'Velvet Matte Lipstick': 'https://images.unsplash.com/photo-1596704017254-9b121068fb31?auto=format&fit=crop&q=80&w=600',
            'Silk Touch Conditioner': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&q=80&w=600',
            'Midnight Rose Perfume': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&q=80&w=600'
        }
    }

    # Update categories (Using URLs directly)
    for slug, url in data['categories'].items():
        Category.objects.filter(slug=slug).update(image=url)

    # Update products (Using URLs directly)
    for name, url in data['products'].items():
        Product.objects.filter(name=name).update(product_image=url)

    print("Images updated successfully!")

if __name__ == '__main__':
    setup_images()
