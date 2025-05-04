from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.db.models import Sum, F
from rds_app.models import *
from rds_app.serializers import *

@ensure_csrf_cookie
def dashboard_view(request):
    total_users = Customer.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total_sum=Sum('total'))['total_sum']
    prod = Product.objects.all()
    products = ProductSerializer(prod, many=True)
    print(products.data)
    top_customers = Order.objects.values(
        user__username=F('customer__user__username'),
        address=F('customer__address')
    ).annotate(total_usage=Sum('total')).order_by('-total_usage')[:5]

    labels = [entry['user__username'] for entry in top_customers]
    usage_data = [float(entry['total_usage']) for entry in top_customers]

 
    payload = {
        'total_users': total_users,
        'total_orders':total_orders,
        'total_revenue':total_revenue,
        "labels": labels,
        "usage_data": usage_data,
        "products": products.data,
    }
    print(payload)
    return render(request, 'frontend/dashboard.html', payload )


@ensure_csrf_cookie
def order_table(request):

    return render(request, 'frontend/order_data.html')