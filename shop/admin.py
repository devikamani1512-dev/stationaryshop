
from django.contrib import admin
from .models import (
    UserProfile,
    CheckoutDetails,
    Order,
    OrderItem,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(CheckoutDetails)
class CheckoutDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'city',
        'pincode',
        'created_at',
    )
    search_fields = ('full_name', 'email', 'phone', 'pincode')
    list_filter = ('state', 'city', 'created_at')
    readonly_fields = ('created_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product_name',
        'quantity',
        'unit_price',
        'item_total',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'user',
        'total_amount',
        'payment_method',
        'payment_status',
        'delivery_status',
        'created_at',
    )

    search_fields = (
        'order_id',
        'user__username',
        'user__email',
    )

    list_filter = (
        'delivery_status',
        'payment_method',
        'payment_status',
        'created_at',
    )

    readonly_fields = (
        'order_id',
        'user',
        'total_amount',
        'created_at',
    )

    list_editable = (
        'delivery_status',
    )

    inlines = [OrderItemInline]

    ordering = ('-created_at',)
