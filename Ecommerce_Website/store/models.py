from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200) 

    def __str__(self):
	    return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)


    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
              url = ''
        return url

    def __str__(self):
	    return self.name
    
class Order(models.Model):
    customer  = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.fetch_total_amount for item in orderitems])
        return total
    
    @property
    def get_items_cart(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total
    
    @property
    def shipping_order(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
            

    def __str__(self):
	    return self.customer.name
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def fetch_total_amount(self):  #get_total
        totals = self.product.price * self.quantity
        return totals 

    def __str__(self):
	    return self.product.name
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200) 
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
	    return self.address