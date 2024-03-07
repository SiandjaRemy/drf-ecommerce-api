from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model

from django.template.defaultfilters import slugify

import uuid

# Create your models here.

User = get_user_model()

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(default=None)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        return super().save(**kwargs)

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    discount = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products_images", blank=True, null=True)
    old_price = models.FloatField(default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="products")
    slug = models.SlugField(default=None)
    inventory = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    top_deal = models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)

    @property
    def price(self):
        if self.discount:
            new_price = self.old_price - (30/100) * self.old_price
        else:
            new_price = self.old_price
        return new_price
    
    def __str__(self):
        return self.name
    
    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)
    

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True ,null=True)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    date_created = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.owner.username}"
    
    @property
    def total_amount(self):
        items = self.order_items.all()
        total = sum([item.quantity * item.product.price for item in items ])
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} - {self.quantity}"
