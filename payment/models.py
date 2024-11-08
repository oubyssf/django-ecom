from django.db import models
from django.contrib.auth.models import User
from store.models import Product
import datetime
from django.core import validators


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.address1+'\n'+self.address2+'\n'+self.city+'\n'+self.state+'\n'+self.zipcode+'\n'+self.country
    
    class Meta:
        verbose_name_plural = 'Shipping addresses'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT, null=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    shipped = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(default=datetime.datetime.now())
    date_shipped = models.DateTimeField(blank=True, null=True)
    invoice = models.CharField(max_length=250, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[validators.MinValueValidator(1)])
    price_paid_per_unit = models.DecimalField(decimal_places=2, max_digits=6)
    def __str__(self):
        return f"(Order #{self.order.pk}) Item: {self.product.name}"