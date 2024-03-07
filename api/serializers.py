from rest_framework import serializers
from store.models import Category, Product, Review, Cart, CartItem, Order, OrderItem
from django.db import transaction



############################################### All Serializers related to Category ###############################################

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]

    
############################################### All Serializers related to Product ###############################################

class AddProductSerializer(serializers.ModelSerializer):
    inventory = serializers.IntegerField(default=0)
    class Meta:
        model = Product
        fields = ["id", "name", "description", "old_price", "discount", "category", "inventory"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    review_count = serializers.SerializerMethodField(method_name="count")
    class Meta:
        model = Product
        fields = ["id", "name", "description", "old_price", "discount", "price", "category", "inventory", "review_count"]

    def count(self, product: Product):
        return product.reviews.all().count()



############################################### All Serializers related Reviews ###############################################

class SimpleReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ["id", "author", "content", "date_created"]
    

class ReviewSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=255)
    class Meta:
        model = Review
        fields = ["id", "content", "date_created"]
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        user = self.context["user"]
        return Review.objects.create(product_id=product_id, author=user, **validated_data)



############################################### All Serializers related CartItems ###############################################
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "discount", "price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "sub_total"]

    def total(self, cart_item: CartItem):
        total = cart_item.quantity * cart_item.product.price
        return total


class AddCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


    def save(self, **kwargs):
        # print(self.validated_data)
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()

            self.instance = cart_item

        except:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


############################################### All Serializers related Cart ###############################################

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="total")
    item_count = serializers.SerializerMethodField(method_name="count")
    class Meta:
        model = Cart
        fields = ["id", "cart_items", "item_count", "grand_total"]
    
    def total(self, cart: Cart):
        items = cart.cart_items.all()
        total = sum([item.quantity * item.product.price for item in items ])
        return total
    
    def count(self, cart: Cart):
        return cart.cart_items.all().count()


############################################### All Serializers related Order items ###############################################

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]



############################################### All Serializers related Orders ###############################################

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="total")
    item_count = serializers.SerializerMethodField(method_name="count")
    class Meta:
        model = Order
        fields = ["id", "order_items", "item_count", "grand_total", "order_status", "creation_date"]
    
    def total(self, order: Order):
        items = order.order_items.all()
        total = sum([item.quantity * item.product.price for item in items ])
        return total
    
    def count(self, order: Order):
        return order.order_items.all().count()


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField(default="")

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id=user_id)

            cart_items = CartItem.objects.filter(cart_id=cart_id)
            order_items = [OrderItem(order_id=order.id, product=item.product, quantity=item.quantity ) for item in cart_items]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()
            return order