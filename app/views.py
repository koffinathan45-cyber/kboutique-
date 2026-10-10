
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from app.models import Product


def index(request):
    products = Product.objects.all()
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(request, "app/index.html", {
        "products": products,
        "cart_count": cart_count,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(request, "app/detail.html", {
        "product": product,
        "cart_count": cart_count,
    })


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method != "POST":
        return redirect("product", slug=slug)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 0

    if quantity < 1:
        messages.error(request, "Choisis une quantité valide.")
        return redirect("product", slug=slug)

    if quantity > product.stock:
        messages.error(request, "Stock insuffisant.")
        return redirect("product", slug=slug)

    cart = request.session.get("cart", {})
    product_id = str(product.id)
    new_quantity = int(cart.get(product_id, 0)) + quantity

    if new_quantity > product.stock:
        messages.error(request, "La quantité dépasse le stock disponible.")
        return redirect("product", slug=slug)

    cart[product_id] = new_quantity
    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, "Produit ajouté au panier !")
    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")
    cart_count = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id).first()

        if product is None:
            continue

        quantity = int(quantity)
        subtotal = Decimal(str(product.price)) * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

        total += subtotal
        cart_count += quantity

    return render(request, "app/cart.html", {
        "items": items,
        "total": total,
        "cart_count": cart_count,
    })


def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Produit retiré du panier.")

    return redirect("cart")
