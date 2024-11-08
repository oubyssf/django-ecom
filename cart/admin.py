from django.contrib import admin
from .models import UserCart

# Register your models here.

class UserCartAdmin(admin.ModelAdmin):
    model = UserCart
    readonly_fields = ["user", 'cart']

admin.site.register(UserCart, UserCartAdmin)
