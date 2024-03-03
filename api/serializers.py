from rest_framework import serializers
from store.models import Category, Product, Review, Cart, CartItem



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
    class Meta:
        model = Product
        fields = ["id", "name", "description", "old_price", "discount", "price", "category", "inventory"]


############################################### All Serializers related Reviews ###############################################

class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=255)
    class Meta:
        model = Review
        fields = ["id", "author_name", "content", "date_created"]
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)



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




