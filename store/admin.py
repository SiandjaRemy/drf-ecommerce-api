from django.contrib import admin
from .models import Category, Product, Review, Cart, CartItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "discount", "old_price", "category", "price", "inventory"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author_name", "product", "date_created"]

class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "date_created"]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "product", "quantity"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)