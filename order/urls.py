from django.urls import path
from .views import checkout, cart

app_name = 'order'

urlpatterns = [
        path('checkout/', checkout, name='checkout'),
        path('cart/', cart, name='cart'),

]
