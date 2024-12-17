from django.shortcuts import render
from products.models import Product, Category
from django.db.models import Avg

PRICE_RANGES = [
    ('0-100', 0, 100),
    ('100-300', 100, 300),
    ('300-500', 300, 500),
    ('500-1000', 500, 1000),
    ('1000-1500', 1000, 1500),
    ('1500-2000', 1500, 2000),
    ('2000-3000', 2000, 3000),
    ('3000-5000', 3000, 5000),
    ('5000-7000', 5000, 7000),
    ('7000-10000', 7000, 10000),
    ('10000-above', 10000, None)
]

STAR_RATINGS = [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
]

def search(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    price_range = request.GET.get('price_range')
    star_rating = request.GET.get('star_rating')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    if price_range:
        for label, min_price, max_price in PRICE_RANGES:
            if price_range == label:
                if max_price is not None:
                    products = products.filter(price__gte=min_price, price__lte=max_price)
                else:
                    products = products.filter(price__gte=min_price)
                break

    if star_rating:
        products = products.annotate(avg_rating=Avg('rating__score')).filter(avg_rating=float(star_rating))

    products = products.annotate(avg_rating=Avg('rating__score'))

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'price_ranges': PRICE_RANGES,
        'star_ratings': STAR_RATINGS,
    }

    return render(request, 'search/search_results.html', context)
