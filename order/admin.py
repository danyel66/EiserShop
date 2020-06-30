from django.contrib import admin
from .models import Order, OrderItem, Payment, Coupon, Refund


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update order to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered',
                    'being_delivered', 'received',
                    'refund_requested', 'refund_granted',
                    'billing_address', 'payment', 'coupon']
    list_display_links = [
        'user',
        'billing_address',
        'payment',
        'coupon'
    ]

    list_filter = ['ordered', 'being_delivered',
                    'received','refund_requested',
                    'refund_granted'
                    ]

    search_fields = [
        'user__username',
        'ref_code',
        'coupon__code'
    ]

    actions = [make_refund_accepted]

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
