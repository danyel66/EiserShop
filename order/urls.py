from django.urls import path
from .views import checkout, cart
from shop.views import OrderSummaryView

app_name = 'order'

urlpatterns = [
        path('checkout/', checkout, name='checkout'),
        path('cart/', OrderSummaryView.as_view(), name='cart'),

]
