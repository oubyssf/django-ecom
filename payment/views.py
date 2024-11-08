from django.shortcuts import render, redirect
from django.urls import reverse
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order
from urllib.parse import urlencode
from django.contrib import messages
from django.conf import settings
import uuid
import requests


def success(request, invoice):
    order = Order.objects.get(invoice=invoice)
    return JsonResponse({"status": order.paid})

def failed(request):
    messages.success(request, "Payment failed")
    return redirect('payment_billing')

def checkout(request):
    login_url = reverse('login')
    query_string =  urlencode({'r': 'payment_checkout'})
    url = '{}?{}'.format(login_url, query_string)
    
    if not request.user.is_authenticated:
        return redirect(url) 

    cart = Cart(request)
    products = cart.get_products()
    quantities = cart.get_quantities()
    total_price = cart.get_total_price()

    if total_price == 0: return redirect('home')

    shipping_addresses = ShippingAddress.objects.filter(user__id=request.user.id)
    
    context = {
        "cart_products": products, 
        "cart_quantities": quantities,
        "total_price": total_price,
        "user_addresses": shipping_addresses,
        "selected_address": request.session.get('selected_address'),
        "form": ShippingForm(request.POST or None)
    }

    return render(request, 'checkout.html', context)

def billing(request):
    if not request.user.is_authenticated:
        return redirect('payment_checkout')
    
    if request.POST:
        cart = Cart(request)
        products = cart.get_products()
        quantities = cart.get_quantities()
        total_price = cart.get_total_price()
        
        if total_price == 0: return redirect('home')

        context = {
            "total_price": total_price, 
            "cart_quantities": quantities, 
            "cart_products": products, 
            'shipping_info': None,
            "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID
        }

        selected_address = request.POST.get('selected_address')
        if selected_address:
            request.session['selected_address'] = selected_address
            context['shipping_info'] = ShippingAddress.objects.get(pk=selected_address)
            return render(request, 'billing.html', context)

        context['shipping_info'] = ShippingAddress(user=request.user)
        shipping_form = ShippingForm(request.POST, instance=context['shipping_info'])
        
        if shipping_form.is_valid():
            shipping_form.save()
            request.session['selected_address'] = context['shipping_info'].pk
            return render(request, 'billing.html', context)
        else:
            messages.error(request, shipping_form.errors)
            context['form'] = ShippingForm(request.POST or None)
            return render(request, 'checkout.html', context)
    
    return redirect('payment_checkout')

    
                       
import json
from django.http import JsonResponse
def create_order(request):
    if not request.method == 'POST' or not request.user.is_authenticated:
        redirect('payment_checkout')

    url = f"{settings.PAYPAL_ENDPOINT}/v2/checkout/orders"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {settings.PAYPAL_ACCESS_TOKEN}"
    }
    cart = Cart(request)
    cart_total = cart.get_total_price()
    selected_address = request.session['selected_address']
    shipping_address = ShippingAddress.objects.get(pk=selected_address)

    invoice = str(uuid.uuid4())
    order_data_json = {
        'intent': "CAPTURE",
        'purchase_units': [{
            'reference_id': invoice,
            'amount': {
                'currency_code': 'USD',
                'value': str(cart_total)
            }
        }]
    }

    data = json.dumps(order_data_json)
    resp = requests.post(url, data=data, headers=headers)
    Order.objects.create(
        user=request.user,
        invoice=invoice,
        total=cart_total,
        shipping_address=shipping_address,
    )
    return JsonResponse(resp.json())

def complete_order(request):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {settings.PAYPAL_ACCESS_TOKEN}"
    }
    body = json.loads(request.body)
    url = f"{settings.PAYPAL_ENDPOINT}/v2/checkout/orders/{body.get('order_id')}/capture"
    resp = requests.post(url, headers=headers)
    resp_data = resp.json()
    invoice = resp_data['purchase_units'][0]['reference_id']
    order = Order.objects.get(invoice=invoice)
    if resp_data['status'] == 'COMPLETED':
        # todo: save paypal order to db
        cart = Cart(request)
        cart.save_as_order_items(order)
        order.paid = True
        order.save()
        cart.clear()
        resp_data['return_url'] = reverse(f"order", args=[invoice])
        return JsonResponse(resp_data)
    
    order.delete()
    resp_data['return_url'] = reverse('payment_failed')
    return JsonResponse(resp_data)