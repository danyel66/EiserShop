from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Item
from .models import Order, OrderItem
from django.utils import timezone

# Create your views here.

def cart(request):
    return render(request, 'orders/order/cart.html')


def checkout(request):
    return render(request, 'orders/order/checkout.html')
