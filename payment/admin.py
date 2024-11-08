from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAddress)

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['date_ordered']
    model = models.Order
    inlines = [OrderItemInline]

admin.site.register(models.Order, OrderAdmin)