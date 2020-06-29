from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from shop.models import Item
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from .forms import CheckoutForm, CouponForm
from shop.views import OrderSummaryView
from .models import Order, OrderItem, BillingAddress, Payment, Coupon

# Create your views here.

import stripe
stripe.api_key = "sk_test_co8XAgMCIPF7uAFZ9O5pWU2I00hX8N3CuH"

def cart(request):
    return render(request, 'orders/order/cart.html')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form=CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order
            }
            return render(self.request, 'orders/order/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("order:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                shipping_address = form.cleaned_data.get('shipping_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                number = form.cleaned_data.get('number')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    shipping_address=shipping_address,
                    apartment_address=apartment_address,
                    country=country,
                    number=number,
                    city=city,
                    zip=zip
                )
                billing_address.save()
                order.billing_address =billing_address
                order.save()

                if payment_option == 'S':
                    return redirect("order:payment", payment_option='Stripe')
                elif payment_option == 'P':
                    return redirect("order:payment", payment_option='PayPal')
                else:
                    messages.warning(self.request, "Failed Checkout")
                    return redirect("order:checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("shop:cart")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                # 'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "orders/order/payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect('order:checkout')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount, #cents
                currency="usd",
                source=token
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.danger(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")

    # messages.warning(self.request, "Invalid data received")
    # return redirect("/payment/stripe/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("order:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered=False)
                order.coupon = get_coupon(request, code)
                order.save()
                messages.success(request, "Successfully added coupon")
                return redirect("order:checkout")
            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order")
                return redirect("order:checkout")
