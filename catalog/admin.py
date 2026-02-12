from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "price", "publisher", "pages", "year", "isbn", "description")
    list_filter = ['genre']
    search_fields = ("title", "author")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total_price", "status")
    list_filter = ("status", "created_at")

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
