from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product
import json

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    products = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.get_total_price()
    return render(request, 'cart.html', {
        "cart_products": products, 
        "cart_quantities": quantities,
        "total_price": total_price,
    })

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        show_msg = product_qty != cart.cart.get(str(product_id), 0)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, product_qty)
        return JsonResponse({ 
            "qty": len(cart), 
            "total_price": cart.get_total_price(),
            'show_msg': show_msg
        })


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        quantities = json.loads(request.POST.get('quantities'))
        cart.update(quantities)
        return JsonResponse({"total_price": cart.get_total_price()})


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        cart.delete(product_id)
        return JsonResponse({"qty": len(cart), 'product_id': product_id, "total_price": cart.get_total_price()})
