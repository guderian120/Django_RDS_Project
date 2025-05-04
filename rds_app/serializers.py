from rest_framework import serializers
from .models import *

"""
Serializers are just functions or classes that take python objects, manipulates them and 
spews up dictionaries or json objects. for instance a CustomerSerializer will take a customer
object from a database and with type <object_customer_database> and return a readerble data like

    {
        'customer1':{'username': 'Andy', 'password':'password_andy'},
        'customer2':{'username': 'Ama', 'password':'password_ama'}
    }

All the classes in this file does this same thing, you can also restrict the attributes of your classes
for instance if you have a model with attrs ['username', 'password', 'email']. serializers can say lets process
only ['username, 'email'] and leave the rest. 

they also validate data, by taking requests, and comparing them to the attributes of a database model to be 
sure if all fields are available before saving data in the database


"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'created_at', 'updated_at']

    




class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class TopCustomerSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)


class MonthlySalesSerializer(serializers.Serializer):
    year = serializers.DateTimeField()
    month = serializers.DateTimeField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)




class AvgOrderByCountrySerializer(serializers.Serializer):
    country = serializers.CharField()
    avg_order = serializers.DecimalField(max_digits=10, decimal_places=2)

class FrequentBuyerSerializer(serializers.Serializer):
    user__username = serializers.CharField()
    order_count = serializers.IntegerField()





class UserSerializer(serializers.ModelSerializer):
    """
    This serializers validates request in order to create a user
    """
    class Meta: 
        model = User # We reference the database module we want to assess
        fields = ['username', 'email', 'first_name', 'last_name', 'password'] # we indicate the fields that should be present in the data
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data): # when we call the serializer.save it will call this method adn create a user
        user = User.objects.create_user(**validated_data)
        return user

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    orders = OrderSerializer(many=True, read_only=True)  # <== This includes orders

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'address', 'loyalty_points', 'orders']


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Customer.objects.create(user=user, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class UnorderedProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class OrderCreateSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)
    

    class Meta:
        model = Order
        fields = ['customer', 'status', 'total']

    def validate_customer(self, value):
        """
        Custom validation to ensure the customer exists based on the username provided.
        This should ensure that the 'customer' field is set automatically.
        """
        username = self.context.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                customer = Customer.objects.get(user=user)
                return customer  # return the actual Customer object
            except (User.DoesNotExist, Customer.DoesNotExist):
                raise serializers.ValidationError("Customer with this username does not exist.")
        return value  # if no username, just return the value passed (i.e., None)
    
    def create(self, validated_data):
        """
        This method is called to create the order and set the customer.
        We ensure the 'customer' is automatically set from the validated data or context.
        """
        customer = validated_data.get('customer')
        if not customer:
            username = self.context.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    customer = Customer.objects.get(user=user)
                    validated_data['customer'] = customer  # Set the customer based on the username
                except (User.DoesNotExist, Customer.DoesNotExist):
                    raise serializers.ValidationError("Customer with this username does not exist.")
        return super().create(validated_data)