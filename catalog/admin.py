from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "price", "publisher", "pages", "year", "isbn", "description")
    list_filter = ['genre']
    search_fields = ("title", "author")

