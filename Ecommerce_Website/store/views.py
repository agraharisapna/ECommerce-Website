from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json 
import datetime



# Create your views here.


def store_view(request):

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()

        cartItems = order.get_items_cart

    else:
        items = []
        order = {'get_cart_total': 0 , 'get_items_cart': 0, 'shipping_order': False}
        cartItems = order['get_items_cart']

    products = Product.objects.all()
    context = {
        "products"  : products,
        "cartItems" : cartItems
    }

    return render(request, 'store/store.html', context)

def cart_view(request):

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_items_cart
    else:
        items = []
        order = {'get_cart_total': 0 , 'get_items_cart': 0, 'shipping_order': False}
        cartItems = order['get_items_cart']


    context = {
        'items' : items,
        'order': order,
        "cartItems" : cartItems
    }

    return render(request, 'store/cart.html', context)

def checkout_view(request):

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_items_cart

    else:
        items = []
        order = {'get_cart_total': 0 , 'get_items_cart': 0, 'shipping_order': False}
        cartItems = order['get_items_cart']


    context = {
        'items' : items,
        'order': order,
        "cartItems" : cartItems,
        
    }


    return render(request, 'store/checkout.html', context)


# not working
def updateItem(request):

    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user.customer 
    product = Product.objects.get(id=productID)

    order, created = Order.objects.get_or_create(customer = customer, comlete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove': 
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item saved.....')


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer = customer, comlete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total():
            order.complete == True
        order.save()

        if order.shipping_order == True:
            ship_record = ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']
            )
            ship_record.save()
    else:
        print("User is not logged in")

    return JsonResponse('Payment submitted..', safe=False)

