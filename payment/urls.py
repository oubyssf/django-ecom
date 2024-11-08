from django.urls import path, include
from . import views

urlpatterns = [
    path('success/<slug:invoice>', views.success, name='payment_success'),
    path('failed/', views.failed, name='payment_failed'),
    path('checkout/', views.checkout, name='payment_checkout'),
    path('billing/', views.billing, name='payment_billing'),
    path('create_order/', views.create_order, name='create_order'),
    path('complete_order/', views.complete_order, name='complete_order'),
]