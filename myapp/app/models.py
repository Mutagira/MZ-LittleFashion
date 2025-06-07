from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

   

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def current_price(self):
     return self.sale_price if self.is_sale else self.price
    
    def __str__(self):
     return self.name
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    
    def __str__(self):
        return self.user.username
    


class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address_line = models.TextField()
    profile = models.OneToOneField(Customer, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.full_name}'s Address"
    
    class Meta:
        verbose_name_plural = 'Shipping Addresses'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
    @property
    def total_price(self):
     return self.quantity * self.product.current_price




class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Card'),
        ('JAZZCASH', 'Jazzcash'),
        ('BANK', 'Bank Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, default=170.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    is_paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f"Order No. {self.id}"
    
    @property
    def product_total(self):
        return self.quantity * self.product.current_price 

    @property
    def total_price(self):
        return self.product_total + self.shipping_cost
    
   
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default="unknown@example.com")
    subject = models.CharField(max_length=200, default="No subject")
    message = models.TextField(default="nothing")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
  