from django.urls import path
from .views import (index, category, contact,
                    single_product, elements, tracking)

app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('category/', category, name='category'),
    path('category/<slug:category_slug>/', category, name='product_list_by_category'),
    path('single-product/<int:id>/<slug:slug>/', single_product, name='single-product'),
    path('contact/', contact, name='contact'),
    path('elements/', elements, name='elements'),
    path('tracking/', tracking, name='tracking'),


]
