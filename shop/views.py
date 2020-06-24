from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from order.models import OrderItem, Order
from django.utils import timezone


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('shop:index')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				email = form.cleaned_data.get('email')
				password1 = form.cleaned_data.get('password1')
				password2 = form.cleaned_data.get('password2')

				messages.success(request, 'Account was created for ' + user)

				return redirect('shop:login')
			else:
				messages.success(request, 'incorrect Password')

		context = {'form':form}
		return render(request, 'shop/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('shop:index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('shop:index')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'shop/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('shop:login')

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


@login_required
def single_product(request, slug):
    product = get_object_or_404(Item, slug=slug)
    return render(request, 'shop/single-product.html',
                            {'product': product})

class OrderSummaryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
				'object': order
			}
			return render(self.request, 'orders/order/cart.html', context)
		except ObjectDoesNotExist:
			messages.warning(self.request, 'You do not have an active order')
			return redirect('/')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check id the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:single-product", slug=slug)
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("shop:single-product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:single-product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("order:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:single-product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:single-product", slug=slug)


@login_required
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check id the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order:cart")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("order:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order:cart")

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:single-product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:single-product", slug=slug)


def elements(request):
    return render(request, 'shop/elements.html')

def tracking(request):
    return render(request, 'shop/tracking.html')
