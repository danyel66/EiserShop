from django.shortcuts import render, get_object_or_404
from .models import Item, Category


# Create your views here.
def index(request):
    context = {
        'items': Item.objects.filter(feature=True)
    }
    return render(request, 'shop/index.html', context)

def category(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Item.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/category.html',
                            {'category': category,
                             'categories': categories,
                             'products': products})

def contact(request):
    return render(request, 'shop/contact.html')


def single_product(request, id, slug):
    product = get_object_or_404(Item, id=id, slug=slug)
    return render(request, 'shop/single-product.html',
                            {'product': product})

def elements(request):
    return render(request, 'shop/elements.html')

def tracking(request):
    return render(request, 'shop/tracking.html')
