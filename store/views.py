from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.http import JsonResponse

def home(request):
    product = Product.objects.all()
    return render(request, "home.html", {"product": product})


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(product=product)
            cart_item.quantity = int(quantity)
            cart_item.save()
            message = "product added to cart successfully" if created else "product quantity updated in the cart."
            return JsonResponse({"status": "success", "message": message})
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "product does not exist."})
    return redirect("home")


def cart(request):
    cart_items = CartItem.objects.all()
    cart_items_count = cart_items.count()  # Get the count of cart items
    return render(request, "cart.html", {"cart_items": cart_items, "cart_items_count": cart_items_count})


def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        return JsonResponse({"status": "success", "message": "Product removed from cart successfully."})
    except CartItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "product does not exist in the cart."})
    return redirect("cart")


