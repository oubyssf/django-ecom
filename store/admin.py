from django.contrib import admin
from django.contrib.auth.models import User
from . import models

admin.site.register(models.Category)
admin.site.register(models.Product)

class ProfileInline(admin.StackedInline):
    model = models.Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    model = models.Profile
    readonly_fields = ["user"]

admin.site.register(models.Profile, ProfileAdmin)