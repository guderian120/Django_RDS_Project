from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from rds_app.models import *

@transaction.atomic
def seed_data(request):
    # Create users
    try:
        alice = User.objects.create_user(username='alice', email='alice@example.com', password='password', first_name='Alice', last_name='Smith')
        bob = User.objects.create_user(username='bob', email='bob@example.com', password='password', first_name='Bob', last_name='Jones')
        charlie = User.objects.create_user(username='charlie', email='charlie@example.com', password='password', first_name='Charlie', last_name='Zhang')

        # Create customers
        c1 = Customer.objects.create(user=alice, address='USA')
        c2 = Customer.objects.create(user=bob, address='Canada')
        c3 = Customer.objects.create(user=charlie, address='UK')

        # # Create categories
        electronics = Category.objects.create(name='Electronics', description='Electronic devices')
        furniture = Category.objects.create(name='Furniture', description='Home and office furniture')
        appliances = Category.objects.create(name='Appliances', description='Home appliances')

        # # Create products
        p1 = Product.objects.create(name='Laptop', category=electronics, price=1200.00, stock=10)
        p2 = Product.objects.create(name='Smartphone', category=electronics, price=800.00, stock=10)
        p3 = Product.objects.create(name='Desk Chair', category=furniture, price=150.00, stock=10)
        p4 = Product.objects.create(name='Coffee Maker', category=appliances, price=85.50, stock=10)

        p1 = Product.objects.create(name='Iphone', category=electronics, price=1200.00, stock=10)
        p2 = Product.objects.create(name='Android', category=electronics, price=800.00, stock=10)
        p3 = Product.objects.create(name='Mattress', category=furniture, price=150.00, stock=10)
        p4 = Product.objects.create(name='Oven', category=appliances, price=85.50, stock=10)

        # Create orders
        o1 = Order.objects.create(customer=c1, status='C', total=1200 + (85.5 * 2), product=p1)  # Completed (Shipped)
        o2 = Order.objects.create(customer=c2, status='P', total=800,product=p1)              # Pending
        o3 = Order.objects.create(customer=c1, status='C', total=150 * 2, product=p1)          # Delivered
        o4 = Order.objects.create(customer=c3, status='X', total=1200, product=p1)             # Cancelled

        # Create order items
        OrderItem.objects.create(order=o1, product=p1, quantity=1, price=1200.00)
        OrderItem.objects.create(order=o1, product=p4, quantity=2, price=85.50)
        OrderItem.objects.create(order=o2, product=p2, quantity=1, price=800.00)
        OrderItem.objects.create(order=o3, product=p3, quantity=2, price=150.00)
        OrderItem.objects.create(order=o4, product=p1, quantity=1, price=1200.00)

        return JsonResponse({'message': 'Data seeded successfully'})
    except Exception as e:
        return JsonResponse({'message': f'OOps an error was encountered with error: {str(e)} you probably have data here already populated '})

