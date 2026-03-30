from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)
    shop_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=30, unique=True)
    
    shop_image = models.ImageField(upload_to="shop_images/", blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    
class Visitor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)
    username = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=100, blank=True)   # ✅ ADD THIS
    location = models.CharField(max_length=100, blank=True)  # ✅ ADD
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)   # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name



class Purchase(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)  # NEW
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
    
    
class Feedback(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.visitor.first_name} for {self.shopkeeper.shop_name}"
    
    
    
    
class CrowdDetection(models.Model):
    location_name = models.CharField(max_length=100)
    people_count = models.IntegerField()  
    crowd_percentage = models.IntegerField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location_name} - {self.crowd_percentage}%"
    
    
