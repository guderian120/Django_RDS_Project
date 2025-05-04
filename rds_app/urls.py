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
    path("customers/", CustomerList.as_view(), name='customer-list'), # This api endpoint ingest a get request, initiates a serializers to cleans and return all customer objects in the database
    path("analytics/", AnalyticsAPIView.as_view(), name='analytics-api'), # This api endpoint ingest a get request, runs complex database queries and returns results like top costumers, overall sales
    path('add-customer/', AddCustomerView.as_view(), name='add-customer'), # This Api endpoint ingest a post request containing information about a customer to be created, it then validates and creates it
    path('add-order/', AddOrderView.as_view(), name='add-order'),   # This Api endpoint ingest a post request containing data on an incoming customer order
    path('products/', ProductList.as_view(), name='products'),   # This Api endpoint ingest a get request and returns all available products in database
    path('seed_data', cmd.seed_data, name="seed_data"), #This Api endpoint ingest a get request and populates database with predefined data
    path('orders/<str:user_name>/', CustomerOrdersView.as_view(), name='customer_orders'), #This Api endpoint returns the order data of a specific customer
    # Documentation endpoints
    path('schema/', SpectacularAPIView.as_view(), name='schema'), #endpoint to download yaml schema
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # endpont to access swagger docs ui
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # endpoint to access redoc ui
]