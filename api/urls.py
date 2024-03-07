from django.urls import include, path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("categories", views.CategoryModelViewset, basename="categories")
router.register("products", views.ProductModelViewset, basename="products")
router.register("cart", views.CartGenericViewset, basename="cart")
router.register("orders", views.OrderModelViewset, basename="order")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewModelViewset, basename="product-reviews")

cart_router = routers.NestedDefaultRouter(router, "cart", lookup="cart")
cart_router.register("items", views.CartItemModelViewset, basename="cart-items")

order_router = routers.NestedDefaultRouter(router, "orders", lookup="order")
order_router.register("items", views.OrderItemModelViewset, basename="order-items")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    path("", include(order_router.urls)),
]