from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from django.db.models import Sum, Count, Avg, F
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *



class CustomerList(APIView):
    """
    This view will return a json of all available customers in the database
    """
    def get(self, request):
        customers = Customer.objects.all() # query database to extract all objects in Customer Table

        # use a custom serializer to convert database objects to python dictionary to export as json
        serializer = CustomerSerializer(customers, many=True)
        # Return an http response objects with serialized data
        return Response(serializer.data)





class CustomerOrdersView(APIView):
    """
    This view returns the order data of a particular customer whose username was 
    passed from the front end, so the url of this view accepts user_name as an argument 

    """
    def get(self, request, user_name): # handle get requests
        # Process received data to extract only username
        username = user_name.split(" ")[0]
        #Query Database to get the customer by username
        customer = Customer.objects.get(user=User.objects.get(username=username))
        # get all orders of the particular customer
        orders = Order.objects.filter(customer=customer)
        # sanitize database objects to python dicts for send as json
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)




class ProductList(APIView):
    """
    This functin returns all available products in the database
    """
    def get(self, request):
        queryset = Product.objects.all() # Query the database to extract data
        serializer_class = ProductSerializer(queryset, many=True) # sanitize database objects
        # return a sanitized json
        return Response(serializer_class.data)



class AnalyticsAPIView(APIView):
    """
    This function runs complex database queries to return information like
        - Top Customers in our database
        - Our overall monthly sales
        - All products in our database
        - Average order by Customer location/country
        -frequent buyers
    """
    def get(self, request): # handle get requests
        # We will extract the top customers by querying their orders
        top_customers = Order.objects.values(customer_name=F('customer__user__username')) \
            .annotate(total_spent=Sum('total')) \
            .order_by('-total_spent')[:5] 
        # return the top five with highest orders
        # We will run database queries on all orders in a particular range to get the montly sales
        monthly_sales = Order.objects.filter(status='C') \
            .annotate(month=TruncMonth('created_at'), year=TruncYear('created_at')) \
            .values('month', 'year') \
            .annotate(total_sales=Sum('total')) \
            .order_by('-year', '-month')

        # Products Never Ordered
        unordered_products = Product.objects.filter(orderitem__isnull=True).values('id', 'name')

        # Average Order by Country
        avg_order_by_country = Order.objects.values(country=F('customer__address')) \
            .annotate(avg_order=Avg('total'))

        # Frequent Buyers 
        frequent_buyers = Customer.objects.annotate(order_count=Count('orders')) \
            .filter(order_count__gt=1) \
            .values('user__username', 'order_count')
        # We return a json response of all the complex queries to be accessible at the localhost:8000/api/analytics endpoint
        return Response({
            "top_customers_by_spending": TopCustomerSerializer(top_customers, many=True).data,
            "monthly_sales_report": MonthlySalesSerializer(monthly_sales, many=True).data,
            "products_never_ordered": UnorderedProductSerializer(unordered_products, many=True).data,
            "average_order_value_by_country": AvgOrderByCountrySerializer(avg_order_by_country, many=True).data,
            "frequent_buyers": FrequentBuyerSerializer(frequent_buyers, many=True).data
        })


class AddCustomerView(APIView):

    """
    This view is used to add Customers to our Database
    we will bypass any authentication requiremnt since our app doesnt have JWT configured
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    #Handle all post  requests to create users
    def post(self, request):
        """
        Extract customer data from incoming request to create the customer
        """
        customer_data = {
            "phone": request.data.get("phone", ''),
            "address": request.data.get("address", ''),
            "loyalty_points": request.data.get("loyalty_points", 0),
        }
        try: # try to create the customer
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                customer = Customer.objects.create(user=user, **customer_data)
                customer_serializer = CustomerSerializer(customer)
                return Response({
                "user": user_serializer.data,
                "customer": customer_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e: #if there are any errors while creating the customer
        # return the errors we encounterd
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddProductView(APIView):
    """
    This is a view to add Products in our database
    """
    def post(self, request): # handle all post request
        """
        pass all incoming data to a serializer to sanitize and validate it
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(): # if data meets all our expectations then it is valid
            serializer.save() # save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED) # return a positive response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # if data is not as we expected, return an error

class AddOrderView(APIView):
    """
    This is a view to add orders to a user or customer account
    we will bypass authentications
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    def post(self, request): # handle post requests
        # try to create others but also stay alert for errors
        try:
            username = request.data.get('customer_id').split(" ")[0] # manipulate incoming request to extract username
            if not username:
                return Response({'detail': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST) # if there is no username in request, return error
            
            serializer = OrderCreateSerializer(data=request.data, context={'username': username}) # sanitize the received request
            if serializer.is_valid(): # If our recieved request is valid 
                serializer.save() # save to database
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e: # if any errors occurs through the process
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # return an error

 