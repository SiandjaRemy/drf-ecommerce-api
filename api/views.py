from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from store.models import Category, Product, Cart, CartItem, Review, Order, OrderItem
from .serializers import (
    CategorySerializer,
    AddProductSerializer,
    ProductSerializer,
    ReviewSerializer,
    SimpleReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    CreateOrderSerializer,
    OrderItemSerializer,
)
from .filters import ProductFilter
from .permisions import IsAuthenticatedAndIsAdminUserOrReadOnly, IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class CategoryModelViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedAndIsAdminUserOrReadOnly]

    @swagger_auto_schema(tags=["category"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["category"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["category"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["category"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["category"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["category"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductModelViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedAndIsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["old_price"]
    pagination_class = PageNumberPagination


    def get_serializer_class(self):
        if self.request.method != "GET":
            return AddProductSerializer
        return ProductSerializer
    
    @swagger_auto_schema(tags=["products & reviews"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ReviewModelViewset(viewsets.ModelViewSet):
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get("product_pk")
        product_reviews = Review.objects.filter(product_id=product_id)
        return product_reviews
    

    def get_serializer_context(self):
        product_id = self.kwargs.get("product_pk")
        user = self.request.user
        # context = {"product_id": product_id} if product_id else {}
        context = {
            "product_id": product_id,
            "user": user
        }
        return context

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SimpleReviewSerializer
        return ReviewSerializer
    
    @swagger_auto_schema(tags=["products & reviews"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["products & reviews"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CartGenericViewset(viewsets.GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = []
    
   
    @swagger_auto_schema(tags=["cart & cart items"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CartItemModelViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = []

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_pk")
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        return cart_items
    

    def get_serializer_context(self):
        cart_id = self.kwargs.get("cart_pk")
        context = {"cart_id": cart_id}
        return context
    

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["cart & cart items"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderModelViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)
    
    def get_serializer_context(self):
        conext = {"user_id": self.request.user.id}
        return conext
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer


    @swagger_auto_schema(tags=["orders & order items"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderItemModelViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(tags=["orders & order items"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["orders & order items"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
