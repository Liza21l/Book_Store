from django.db import models
from django.contrib.auth.models import User
import django_filters
from django import forms



class Product(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="img/", blank=True, null=True)


    def __str__(self):
        return self.title
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} — {self.product.title}"


class ProductFilter(django_filters.FilterSet):
    genre = django_filters.MultipleChoiceFilter(
        field_name="genre",
        choices=[
            ("fantasy", "Fantasy"),
            ("detective and thriller", "Detective And Thriller"),
            ("romance", "Romance"),
            ("business and self-development", "Business And Self-Development"),
            ("children's literature", "Children's Literature"),
        ],
        widget=django_filters.widgets.forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Product
        fields = ["genre"]

class Order(models.Model):
    STATUS_CHOICES = [
        ("processing", "В обробці"),
        ("shipping", "В доставці"),
        ("delivered", "Доставлено"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="processing"
    )

    def __str__(self):
        return f"Замовлення #{self.id} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
