from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Product, Rating
from .forms import RatingForm
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.annotate(avg_rating=Avg('rating__score'))
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ratings = Rating.objects.filter(product=product)
    average_rating = ratings.aggregate(Avg('score'))['score__avg']

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('product_detail', pk=product.pk)
    else:
        rating_form = RatingForm()

    context = {
        'product': product,
        'ratings': ratings,
        'rating_form': rating_form,
        'average_rating': average_rating,
    }
    return render(request, 'products/product_detail.html', context)
