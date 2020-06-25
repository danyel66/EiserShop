from django.urls import path
from order.views import CheckoutView
from shop.views import OrderSummaryView


app_name = 'order'

urlpatterns = [
        path('checkout/', CheckoutView.as_view(), name='checkout'),
        path('cart/', OrderSummaryView.as_view(), name='cart'),

]
