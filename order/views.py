from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Item
from django.utils import timezone
from django.views.generic import View
from .forms import CheckoutForm
from .models import Order, OrderItem, BillingAddress

# Create your views here.

def cart(request):
    return render(request, 'orders/order/cart.html')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form=CheckoutForm()
        context={
            'form': form
        }
        return render(self.request, 'orders/order/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            # same_shipping_address = form.cleaned_data.get('same_shipping_address')
            # save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')
            billing_address = BillingAddress(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip
            )
            billing_address.save()
            order.billing_address =billing_address
            order.save()
            return redirect("order:checkout")
        message.warning(self.request, "Failed checkout")
        return redirect("order:checkout")
