from django.contrib.auth.models import User
from store.models import Product
from .models import UserCart
from payment.models import OrderItem
import json


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        
        self.session['session_key'] = self.session.get('session_key', {})

        if self.user.is_authenticated:
            user_cart, created = UserCart.objects.get_or_create(
                user=User.objects.get(id=request.user.id)
            )
            
            if created or self.session['session_key'] != {}:
                user_cart.cart = json.dumps(self.session['session_key'])    
            
            user_cart.save()
            self.session['session_key'] = json.loads(user_cart.cart)
        
        self.cart = self.session.get('session_key')


    def get_products(self):
        product_ids = self.cart.keys()
        products =  Product.objects.filter(id__in=product_ids)
        return products
    
    
    def get_quantities(self):
        return self.cart
    
    def get_total_price(self):
        total_price = 0
        products = self.get_products()
        for product in products:
            qty = self.cart[str(product.id)]
            price = product.sale_price if product.on_sale else product.price
            price = float(price)
            total_price += qty * price
        return round(total_price, 2)

    def save(self):
        if self.user.is_authenticated:
            user_cart, _ = UserCart.objects.get_or_create(user=self.user,)
            user_cart.cart = json.dumps(self.cart)
            user_cart.save()
    
    def save_as_order_items(self, order):
        for product_id, qty in self.get_quantities().items():
            product = Product.objects.get(pk=product_id)
            price = product.sale_price if product.on_sale else product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price_paid_per_unit = price
            )
    
    def add(self, product, quantity):
        product_id = str(product.id)
        self.cart[product_id] = int(quantity)
        self.session.modified = True
        self.save()


    def update(self, quantities):
        for id in quantities:
            self.cart[str(id)] = int(quantities[id])
        
        self.session.modified = True
        self.save()
        
    def delete(self, product_id):
        _id = str(product_id)
        if _id in self.cart:
            del self.cart[_id]
            self.session.modified = True

        self.save()

    def clear(self):
        self.cart = {}
        self.session['session_key'] = {}
        self.save()

    def __len__(self):
        return len(self.cart)
    
    def __str__(self):
        products = self.get_products()
        s = ["{} ({})".format(p.name, self.cart[str(p.id)]) for p in products]
        return ' + '.join(s)