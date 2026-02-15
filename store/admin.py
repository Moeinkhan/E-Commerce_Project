from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory', 'collection']
    list_filter = ['collection']
    search_fields = ['title']
    list_editable = ['price', 'inventory']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_filter = ['payment_status']
    search_fields = ['customer__first_name', 'customer__last_name']


admin.site.register(Promotion)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)