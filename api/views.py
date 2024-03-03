from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from store.models import Category, Product, Cart, CartItem, Review
from .serializers import (
    CategorySerializer,
    AddProductSerializer,
    ProductSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)
from .filters import ProductFilter

# Create your views here.


class CategoryModelViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductModelViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["old_price"]
    pagination_class = PageNumberPagination


    def get_serializer_class(self):
        if self.request.method != "GET":
            return AddProductSerializer
        return ProductSerializer


class ReviewModelViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_pk")
        product_reviews = Review.objects.filter(product_id=product_id)
        return product_reviews
    

    def get_serializer_context(self):
        product_id = self.kwargs.get("product_pk")
        # context = {"product_id": product_id} if product_id else {}
        context = {"product_id": product_id}
        return context


class CartGenericViewset(viewsets.GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemModelViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

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
