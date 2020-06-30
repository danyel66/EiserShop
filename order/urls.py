from django.urls import path
from order.views import CheckoutView, PaymentView, AddCouponView, RequestRefundView
from shop.views import OrderSummaryView


app_name = 'order'

urlpatterns = [
        path('checkout/', CheckoutView.as_view(), name='checkout'),
        path('cart/', OrderSummaryView.as_view(), name='cart'),
        path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
        path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
        path('request-refund/', RequestRefundView.as_view(), name='request-refund'),

]
