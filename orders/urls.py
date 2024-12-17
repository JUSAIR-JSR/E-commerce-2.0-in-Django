from django.urls import path
from . import views

urlpatterns = [
    path('order_history/', views.order_history, name='order_history'),
    path('checkout/', views.checkout, name='checkout'),
]
