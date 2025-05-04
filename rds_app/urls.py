from django.urls import path 
# Import all functions in your views
from .views import *
# import the documentation framework
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# The commands in the management dir will be used to perform task like database populating, testing out endpoints amongs others
from rds_app.management.commands import seed_data as cmd # getting our commands in management directory 

"""
This url creates routes for our api
"""

urlpatterns = [
    path("customers/", CustomerList.as_view(), name='customer-list'), # path to return all costumers in a json
    path("analytics/", AnalyticsAPIView.as_view(), name='analytics-api'), # path to run complex sql queries and return 
    path('add-customer/', AddCustomerView.as_view(), name='add-customer'), # path to add a customer
    path('add-order/', AddOrderView.as_view(), name='add-order'),   # path to add an order ProductList
    path('products/', ProductList.as_view(), name='products'),   # path to add an order 
    path('seed_data', cmd.seed_data, name="seed_data"), #this url is used to populate our database
    path('orders/<str:user_name>/', CustomerOrdersView.as_view(), name='customer_orders'), # path  to return order data of a particular user
    # Documentation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'), #endpoint to download yaml schema
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # endpont to access swagger docs ui
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # endpoint to access redoc ui
]