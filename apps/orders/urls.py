from django.urls import path
from .views import cart_view, add_to_cart_view, remove_from_cart_view, checkout_view

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
]
