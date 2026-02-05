from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()
    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            products = Product.objects.filter(title__icontains=search)

    return render(request, "home.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def my_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("product_list")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user = request.user,
        product=product,
        defaults={"quantity": 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("product_detail", pk=pk)

@login_required
def cart(request):
    cart = CartItem.objects.filter(user=request.user)
    return render(request, "cart.html", {"cart": cart})