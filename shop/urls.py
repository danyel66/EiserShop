from django.urls import path
from .views import (index, category, contact,
                    single_product, elements, tracking, add_to_cart, remove_from_cart,
                    registerPage, loginPage, logoutUser, add_single_item_to_cart, remove_single_item_from_cart
                    )

app_name = 'shop'

urlpatterns = [
    path('register/', registerPage, name="register"),
	path('login/', loginPage, name="login"),
	path('logout/', logoutUser, name="logout"),

    path('', index, name='index'),
    path('category/', category, name='category'),
    path('category/<slug:category_slug>/', category, name='product_list_by_category'),
    path('single-product/<slug>/', single_product, name='single-product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('add-item-to-cart/<slug>/', add_single_item_to_cart,
         name='add-single-item-to-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('contact/', contact, name='contact'),
    path('elements/', elements, name='elements'),
    path('tracking/', tracking, name='tracking'),


]
