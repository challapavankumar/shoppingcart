from django.db import models
from  django.contrib.auth.models import User
# Create your models here.
class AdminUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='admin/products')
    mobile=models.CharField(max_length=10)
    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    address=models.CharField(max_length=200,null=True,blank=True)
    joined_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name
class Category(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products')
    marked_price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField()
    description=models.TextField()
    warranty=models.CharField(max_length=200,null=True,blank=True)
    return_policy=models.CharField(max_length=200,null=True,blank=True)
    view_count=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/')
    def __str__(self):
        return self.product.title
class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    total=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Cart:"+str(self.id)
class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()

    def __str__(self):
        return "Cart:"+str(self.id)+"CartProduct:"+str(self.id)
Order_Status=(
    ('Order Received','Order Received'),
    ('Order Processing','Order Processing'),
    ('On the way','On the way'),
    ('Order completed','Order completed'),
    ('Order Canceled','Order Canceled'),

)
METHOD=(
    ('cashondelivary','cashondelivary'),
    ('khalti','kalthi'),


)


class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    ordered_by=models.CharField(max_length=200)
    shipping_adress=models.CharField(max_length=200)
    mobile=models.CharField(max_length=10)
    email=models.EmailField()
    subtotal=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    total=models.PositiveIntegerField()
    order_status=models.CharField(max_length=30,choices=Order_Status)
    created_at=models.DateTimeField(auto_now_add=True)
    payment_method=models.CharField(max_length=30,choices=METHOD,default='cashondelivary')
    payment_completed=models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return "Order:"+str(self.id)
