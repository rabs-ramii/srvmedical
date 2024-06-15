from django.db import models

# Create your models here.

class User(models.Model):
    email=models.CharField(primary_key=True,max_length=100)
    mobile_no=models.CharField(max_length=15)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    gender=models.CharField(max_length=20)


class Product(models.Model):
    id=models.BigAutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    quantity=models.CharField(max_length=50)
    product_desc=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.DecimalField(max_digits=10,decimal_places=2)
    availability=models.BooleanField(default=True)
    image=models.FileField(upload_to="product_img",max_length=250, null=True, default=None)
    category=models.CharField(max_length=50)

class Cart(models.Model):
    id=models.BigAutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()

class Order(models.Model):
    id=models.BigAutoField(primary_key=True)
    user=models.CharField(max_length=50)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    prescription=models.FileField(upload_to="prescriptions",max_length=250, null=True, default=None)
    quantity=models.IntegerField()
    discount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_method=models.CharField(max_length=50)
    payment_status=models.CharField(default="Pending",max_length=50)
    delivery_address=models.CharField(max_length=250)
    delivery_status=models.CharField(default="Dispatch Soon",max_length=50)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class AboutUs(models.Model):
    id=models.BigAutoField(primary_key=True)
    email=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    address=models.CharField(max_length=100)
    description=models.CharField(max_length=250)



