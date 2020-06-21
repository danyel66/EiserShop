from django.shortcuts import render

# Create your views here.

def cart(request):
    return render(request, 'orders/order/cart.html')


def checkout(request):
    return render(request, 'orders/order/checkout.html')
