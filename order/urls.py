from django.urls import path
from order.views import CheckoutView, PaymentView, add_coupon
from shop.views import OrderSummaryView


app_name = 'order'

urlpatterns = [
        path('checkout/', CheckoutView.as_view(), name='checkout'),
        path('cart/', OrderSummaryView.as_view(), name='cart'),
        path('add-coupon/', add_coupon, name='add-coupon'),
        path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),


]
