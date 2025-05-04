# frontend/urls.py
from django.urls import path
from .views import dashboard_view, order_table

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path("order-table/", order_table, name="order-table"),
]
