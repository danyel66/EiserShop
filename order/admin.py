from django.contrib import admin
from .models import Order, OrderItem, Payment, Coupon


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)

# # Register your models here.
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'email',
#                     'address', 'postal_code', ]
#     list_filter = ['paid', 'created', 'updated']
