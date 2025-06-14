from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
# shop/models.py





class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Memory(models.Model):
    size = models.CharField(max_length=4, choices=[
        ('8GB', '8GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB')
    ])

    def __str__(self):
        return self.size

class SSD(models.Model):
    size = models.CharField(max_length=5, choices=[
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB')
    ])

    def __str__(self):
        return self.size

class Processor(models.Model):
    type = models.CharField(max_length=5, choices=[
        ('Intel', 'Intel'),
        ('AMD', 'AMD')
    ])
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type} {self.name}"

class Laptop(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)  # One-to-many relationship
    memory = models.ManyToManyField(Memory)  # Many-to-many relationship
    ssd = models.ManyToManyField(SSD)  # Many-to-many relationship
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)  # One-to-many relationship
    description = models.TextField()
    image=models.ImageField(upload_to='images/',default='images/default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
   
    def __str__(self):
        return self.name






class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Folosește User standard Django
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    laptop = models.ForeignKey('Laptop', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.laptop.name}"
    