from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
import datetime

@receiver(pre_save, sender=Order)
def set_date_shipped_on_update(sender, instance, **kwargs):
    if instance.pk:
        obj = Order.objects.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = datetime.datetime.now()

        if not instance.shipped and obj.shipped:
            instance.date_shipped = None

    
    